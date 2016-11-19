#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# fuer die komandozeilenargumente
from sys import argv
# GPIOs:
import RPi.GPIO as GPIO
# "its all about time"
from time import time, sleep
# UDP Communication
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

# Globale Variabeln:
spielName = "Schwebedraht"
spielNameZusatz = "Ein Spiel der see-base"
version = "0.2"
startzeit = 1337
segmente = {
    "start": [12],
    "bonus": [18, 24, 29, 33],
    "fail": [16, 22, 26, 31, 35],
    "ende": [37]
}
zeitenListe = []
debug = False
demo = False

# komandozeilenargumente
for i in argv:
    if i in ["--help", "-h", "/h", "/help", "?", "h"]:
        print("\n"+spielName+" - "+spielNameZusatz+"\n")
        print("Quelle: https://github.com/see-base/schwebedraht\n\n")
        print("Moegliche Befehle:\n\t--help\t- Zeigt diese Hilfe an")
        print("\t-v\t- Zeigt die Version des Spieles")
        print("\t--debug\t- Debug Modus...")
        print("\t--demo\t- Demo Modus")
        print("\n")
        exit()
    elif i == "-v":
        print("\n{0} - {1}\n\nVersion:\t{2}\n".format(spielName, spielNameZusatz, version))
        exit()
    elif i == "--debug":
        debug = True
    elif i == "--demo":
        demo = True

def main():
    while True:
        for key, value in segmente.items():
            for pin in value:
                if debug: print("main():for key, value in segmente.items():for pin in value:pin = "+str(pin))
                if not GPIO.input(pin):
                    get_time(key, pin)
                    if key == "start":
                        start()
                    elif key == "bonus":
                        pass
                    elif key == "fail":
                        pass
                    elif key == "ende":
                        pass

def get_time(name, pin):
    global startzeit
    
    if name == "start": startzeit = time()
    else: zeitenListe.append((pin, time()))

def start():
    sock.send(bytes("medien/effektderpunkteausblendetderbaldkommt:" + str(True), "UTF-8"))
    #effekt_countdown_Spielstart

def ende():
    # Statistiken fuer das Ende
    # Genaue Aufschl√sselung des extrem komplizierten und geilen Punktesystem
    pass
    # zur√cksetzen

def bonus():
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("star.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
    
def fail():
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("pesthorn.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
    
if demo:
    while True:
        sock.send(bytes("medien/punkte/punkte:start", "UTF-8"))
        sleep(5)
        if debug: print("start()")
        start()
        sock.send(bytes("medien/punkte/punkte:start", "UTF-8"))
        sleep(5)
        if debug: print("bonus()")
        bonus()
        sock.send(bytes("medien/punkte/punkte:42", "UTF-8"))
        sleep(5)
        if debug: print("fail()")
        fail()
        sock.send(bytes("medien/punkte/punkte:1337", "UTF-8"))
        sleep(5)
        if debug: print("ende")
        sock.send(bytes("medien/punkte/punkte:ende", "UTF-8"))
        ende()
        sleep(5)

else:
    main()
