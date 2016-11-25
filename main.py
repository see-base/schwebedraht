#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#

from sys import argv # fuer die kommandozeilenargumente
import RPi.GPIO as GPIO # raspi gpio-pins
from time import time, sleep # fuer zeitmessung und pausen
from random import randint # fuers punktesystem
import math
import socket # udp-kommunikation

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

startzeit = 0.0
zeitenListe = []

debug = False
demo = False

punkte = 0
p_multiplikator = 1

# UDP-Socket einstellen
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

# GPIOs einstellen
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
for key, value in segmente.items():
	GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# funktions-schleife:
# -> warte auf input
# -> speichere die zeit für den input
# -> ermittle die punkte
# -> zeige einen effekt

def main():

    if demo:
        while True:
            for s in ["start", "bonus", "fail", "bonus", "bonus", "fail", "bonus", "ende"]:
                get_time(s, segmente[s][randint(0, len(segmente[s]) - 1)])
                sock.send(bytes("medien/punkte/punkte:{} | {}".format(punkte, p_multiplikator), "UTF-8"))
                if s == "start": start()
                elif s == "bonus": bonus()
                elif s == "fail": fail()
                elif s == "ende": ende()
                sleep(5)

    while True:
        for key, value in segmente.items():
            for pin in value:
                if not GPIO.input(pin):
                    if debug: print("\nPin {} wurde berührt | Key = {}".format(pin, key))
                    get_time(key, pin)
                    if key == "start":
                        #reset() -- bin hier noch auf käferjagt...
                        start()
                    elif key == "bonus":
                        bonus()
                    elif key == "fail":
                        fail()
                    elif key == "ende":
                        ende()
                    sleep(0.2)

# zeitmessung
def get_time(name, pin):
    global startzeit, zeitenListe
    zeit = time()

    if debug:
        print("Zeitstempel:", zeit - startzeit) if startzeit != 0.0 else print("Zeitstempel:", startzeit)
    if name == "start":
        startzeit = zeit
        zeitenListe.append((pin, zeit - startzeit))
    else:
        zeitenListe.append((pin, zeit - startzeit))
        if zeitenListe[-1][1] - zeitenListe[-2][1] > 1:
            punkte_setzen(zeitenListe[-1], zeitenListe[-2])
        else: zeitenListe.pop()

# funktionen fuer effekte
def start():
    if debug: print("start()")
    #effekt_countdown_Spielstart

def ende():
    if debug: print("ende()")
    # Statistiken fuer das Ende
    # Genaue Aufschlüsselung des extrem komplizierten und geilen *hust hust* Punktesystem

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

    if pin1 in segmente["bonus"] and pin2 != pin1:
        if zeit1 - zeit2 <= 5:   # m. verdoppelt sich bis 5 sek
            p_multiplikator *= 2
        elif zeit1 - zeit2 <= 10: # m. erhoeht sich um 1 bis 10 sek
            p_multiplikator += 1
        elif zeit1 - zeit2 >= 15: # m. wird zurueckgesetzt ab 15 sek
            p_multiplikator = 1

        punkte += randint(10, 50) * p_multiplikator # punke setzen

    elif pin1 in segmente["fail"]:
        if p_multiplikator > 1: # bei beruehrung wird m. halbiert
            p_multiplikator = math.ceil(p_multiplikator / 2)

    sock.send(bytes("medien/punkte/punkte:{} | {}".format(punkte, p_multiplikator), "UTF-8"))
    if debug: print("Punkte: {} | Multiplikator: {}".format(punkte, p_multiplikator))

def reset():
    if debug: print("reset")
    global startzeit, zeitenListe, punkte, p_multiplikator
    startzeit = 0.0
    zeitenListe = []
    punkte = 0
    p_multiplikator = 1

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

try:
    main()
except KeyboardInterrupt:
    # diese zeile spaeter durch reset-funktion beim start ersetzen.
    sock.send(bytes("medien/punkte/punkte:0 | 1", "UTF-8"))
