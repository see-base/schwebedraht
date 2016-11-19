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

#gpios einstellen
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
for key, value in segmente.items():
	GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# komandozeilenargumente
for i in argv:
    if i in ["--help", "-h", "/h", "/help", "?", "h"]:
        print("\n{0} - \n".format(spielName, spielNameZusatz))
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
                if not GPIO.input(pin):
                    if debug: print("\nPin {} wurde berührt | Key = {}".format(pin, key))
                    get_time(key, pin)
                    if key == "start":
                        start()
                    elif key == "bonus":
                        bonus()
                    elif key == "fail":
                        fail()
                    elif key == "ende":
                        ende()
                    sleep(0.1)

def get_time(name, pin):
    global startzeit

    if name == "start": startzeit = time()
    else: zeitenListe.append((pin, time() - startzeit))
    if debug: print("Zeitstempel:", time() - startzeit)

def start():
    if debug: print("start()")
    #effekt_countdown_Spielstart

def ende():
    if debug: print("ende()")
    # Statistiken fuer das Ende
    # Genaue Aufschl�sselung des extrem komplizierten und geilen Punktesystem
    pass
    # zurücksetzen

def bonus():
    if debug: print("bonus()")
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("star.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))

def fail():
    if debug: print("fail()")
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("pesthorn.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))

if demo:
    while True:
        for s in ["start", "42", "1337", "ende"]:
            sock.send(bytes("medien/punkte/punkte:" + s, "UTF-8"))
            if s == "start": start()
            elif s == "42": bonus()
            elif s == "1337": fail()
            elif s == "ende": ende()
            sleep(5)

else:
    main()
