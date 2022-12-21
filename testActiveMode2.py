import string
from unittest import result
import mysql.connector
from serial import *

PRESET_Value = 0xFFFF
POLYNOMIAL = 0x8408

test_serial = Serial('COM11', 57600, timeout=0.1)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="crud_db"
)

mycursor = mydb.cursor()


#scan
TIDScan = '06 03 01 00 06'  
EPCScan = '04 03 0F' 
#change EPC
writeEpc = '0F 03 04 03 00 00 00 00 11 22 33 44 55 66'
#set Data
setAddress = '05 03 24 00'


def crc(cmd):
    cmd = bytes.fromhex(cmd)
    uiCrcValue = PRESET_Value
    for x in range((len(cmd))):
        uiCrcValue = uiCrcValue ^ cmd[x]
        for y in range(8):
            if (uiCrcValue & 0x0001):
                uiCrcValue = (uiCrcValue >> 1) ^ POLYNOMIAL
            else:
                uiCrcValue = uiCrcValue >> 1
    crc_H = (uiCrcValue >> 8) & 0xFF
    crc_L = uiCrcValue & 0xFF
    cmd = cmd + bytes([crc_L])
    cmd = cmd + bytes([crc_H])
    return cmd


def send_cmd(cmd):
    data = crc(cmd)
    print(data)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    hex_space = " ".join(hex_list)
    print(hex_space)
    
    epcfinal = str(hex_space)


    mycursor.execute("SELECT name FROM users WHERE epc = '%s'" % epcfinal)    
    myresult = mycursor.fetchall()
    for db_name in myresult:
        print(db_name)
    dbi_name = (str(db_name))
    dbia_name = dbi_name.replace("(", "")
    dbis_name = dbia_name.replace("'", "")
    dbid_name = dbis_name.replace(",", "")
    dbif_name = dbid_name.replace(")", "")

    mycursor.execute("SELECT title FROM users WHERE epc ='%s'" % epcfinal)
    myresult = mycursor.fetchall()
    for db_title in myresult:
        print(db_title)
    dbi_title = (str(db_title))
    dbia_title = dbi_title.replace("(", "")
    dbis_title = dbia_title.replace("'", "")
    dbid_title = dbis_title.replace(",", "")
    dbif_title = dbid_title.replace(")", "")

    mycursor.execute("SELECT status FROM users WHERE epc ='%s'" % epcfinal)
    myresult = mycursor.fetchall()
    for db_status in myresult:
        print(db_status)
    dbi_status = (str(db_status))
    dbia_status = dbi_status.replace("(", "")
    dbis_status = dbia_status.replace("'", "")
    dbid_status = dbis_status.replace(",", "")
    dbif_status = dbid_status.replace(")", "")
    
    mycursor.execute("SELECT role FROM users WHERE epc ='%s'" % epcfinal)
    myresult = mycursor.fetchall()
    for db_role in myresult:
        print(db_role)
    dbi_role = (str(db_role))
    dbia_role = dbi_role.replace("(", "")
    dbis_role = dbia_role.replace("'", "")
    dbid_role = dbis_role.replace(",", "")
    dbif_role = dbid_role.replace(")", "")
    
    sql_insert = "INSERT INTO overview (name, title, status, role) VALUES (%s, %s, %s, %s)"
    val = (dbif_name, dbif_title, dbif_status, dbif_role)
    mycursor.execute(sql_insert, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted")



send_cmd(EPCScan)

