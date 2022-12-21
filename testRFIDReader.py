from serial import *

PRESET_Value = 0xFFFF
POLYNOMIAL = 0x8408

ser = Serial('COM11', 57600, timeout=0.1)

while ser.available():
    print (ser.readline())

