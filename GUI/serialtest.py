from serial.serialutil import EIGHTBITS , PARITY_NONE, STOPBITS_ONE, Timeout
import serial
import time
import struct

BAUD = 115200
TIMEOUT = 0.5

# USB Port for right leg: USB7
# USB Port for left leg : USB6

uart = serial.Serial("COM13",baudrate=BAUD,timeout=TIMEOUT,parity=PARITY_NONE,stopbits=STOPBITS_ONE,bytesize = EIGHTBITS)

"""
Right leg:
    rot encoder: inwards = 550 ---  outwards = 950
    hip encoder: down = 650 -----   up = 3100
    knee encoder: down = 500 -----  up = 3200

Left leg:
    rot encoder: inwards = 950 ---  outwards = 500
    hip encoder: down = 2900 -----   up = 170
    knee encoder: down = 3200 -----  up = 500
"""
data = [1,2,3,4,5]

print(data[2].to_bytes(length=1,byteorder='little'))
while True:
    
    #if uart.in_waiting:
        x = uart.read(1)
        # uart.write(data[2].to_bytes(length=1,byteorder='little'))
        # enc_rot = struct.unpack(">H", x[:2])
        # enc_hip = struct.unpack(">H", x[2:4])
        # enc_knee = struct.unpack(">H", x[4:6])
        enc_rot = 5
        enc_hip = 5
        enc_knee = x[0]
        print("rot {} hip {} knee {}".format({enc_rot},{enc_hip},{enc_knee}))