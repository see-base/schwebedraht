#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# sudo pip3 install pyserial
#
# Dieses kleine Script dient zum virtualisieren der WANDler
#
import serial
from random import randint

ser = serial.Serial(
            port='/dev/ttyUSB0',
                baudrate=115200,
                    parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                                xonxoff=serial.XOFF,
                                    rtscts=False,
                                        dsrdtr=False
                                        )

try:
    ser.open()
except:
    print("Serial Port already open")
ser.isOpen()

print("Initializing the device ..")

ser.write(bytes(0x00))

print("Write bytes:")
data="ID:0"+str(randint(0,4))+";INT:0"+str(randint(0,6))+";BAT:"+str(randint(10,99))+";F:"+str(randint(0,4))+"00;\n"
ser.write(bytes(data, "UTF-8"))
print(bytes(data, "UTF-8"))
#ser.write (bytes("ID:42;INT:11;BAT:79;F:100;\n", "UTF-8"))
#print(bytes("ID:42;INT:11;BAT:79;F:100;\n", "UTF-8"))

print('Done')
