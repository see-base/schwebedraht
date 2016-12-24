#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# sudo pip3 install pyserial
#
# Dieses kleine Script dient zum virtualisieren der WANDler
#
import serial, socket
from random import randint
from sys import argv

udp = False
serError = False #Falls es ein error beim seriell gibt
for i in argv:
    for i in argv:
        if i in ["-h", "--help"]:
            print("Dieses kleine Script soll die Kommunikation zwischen den WANDlern und dem PythonSpiel simulieren\n")
            print("Standardmaeßig versucht das Spiel ueber das Device '/dev/ttyUSB0' die Serielle Schnitstelle zu oeffnen\n")
            print("\t--udp\t- fuer Simulation ueber UDP")
            print("\nWeitere Informationen auf github.com/see-base/schwebedraht und im SourceCode")
            exit()
        if i in ["-upd", "--udp"]:
            udp = True
            print("Verwende UDP")

data="ID:0"+str(randint(0,4))+";INT:0"+str(randint(0,6))+";BAT:"+str(randint(10,99))+";F:"+str(randint(0,4))+"00;\n"
ser = False
if not udp:
    try:
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
    except:
        print("Moeglicherweise kein serielles Device angeschlossen")
        serError = True

    if not serError:
        try:
            ser.open()
        except:
            print("Serial Port already open")
        ser.isOpen()
        print("Initializing the device ..")
        ser.write(bytes(0x00))
        print("Write bytes:")
        ser.write(bytes(data, "UTF-8"))
        print(bytes(data, "UTF-8"))
        #   ser.write (bytes("ID:42;INT:11;BAT:79;F:100;\n", "UTF-8"))
        #   print(bytes("ID:42;INT:11;BAT:79;F:100;\n", "UTF-8"))
        print('Done')

if udp:
    # Verbindung via UDP aufbauen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("127.0.0.1", 5005)) 
 
 
    def sende(Nachricht): 
        print( "Nachricht:", Nachricht )
        sock.send(bytes(Nachricht, "UTF-8"))
    sende(data)

