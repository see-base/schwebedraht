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
from random import randint # fuers punktesystem
# UDP Communication
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

# Globale Variabeln:
spielName = "Schwebedraht"
spielNameZusatz = "Ein Spiel der see-base"
version = "0.2"

segmente = {
    "start": [12],
    "bonus": [18, 24, 29, 33],
    "fail": [16, 22, 26, 31, 35],
    "ende": [37]
}

startzeit = None
zeitenListe = []

debug = False
demo = False

punkte = 0
p_multiplikator = 1

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
    elif i in ["-v", "--version"]:
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

# zeitmessung
def get_time(name, pin):
    global startzeit
    if debug: print("Zeitstempel:", time() - startzeit)

    zeit = time()
    if name == "start":
        startzeit = zeit
    else:
        zeitenListe.append((pin, zeit - startzeit))
        punkte_setzen(zeitenListe[-1], zeitenListe[-2])

# funktionen fuer effekte
def start():
    # todo: game-reset einbauen
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

def punkte_setzen(aktuelle_zeit, letzte_zeit):
    global punkte, p_multiplikator

    pin1, zeit1 = aktuelle_zeit
    pin2, zeit2 = letzte_zeit

    if pin1 != pin2:
        if zeit1 - zeit2 < 5:
            p_multiplikator *= 2
        elif zeit1 - zeit2 < 10:
            p_multiplikator += 1

    if pin1 in segmante["bonus"]:
        punkte += randint(100, 300)
    elif pin1 in segmente["fail"] and punkte > 0:
        punkte -= randint(50, 100)

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
