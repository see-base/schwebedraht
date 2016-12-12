#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# Groessere Aenderungen bitte in den READMEs Dokumentieren!
#
from sys import argv # fuer die kommandozeilenargumente
import RPi.GPIO as GPIO # raspi gpio-pins
from time import time, sleep # fuer zeitmessung und pausen
from random import randint # fuers punktesystem
import math
import socket # udp-kommunikation
from pygame import mixer

# Globale Variabeln:
spielName = "Schwebedraht"
spielNameZusatz = "Ein Spiel der see-base"
version = "0.3"

segmente = {
    "start": [12],
    "bonus": [18, 24, 29, 33],
    "fail": [16, 22, 26, 31, 35],
    "ende": [37]
}

startzeit = 0.0
zeitenListe = []

running = False

debug = False
demo = False
audio = True

punkte = 0
p_multiplikator = 1

def setup():
    global audio, sock
    # UDP-Socket einstellen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("127.0.0.1", 4444))
    if debug: print("UDP-Socket eingestellt")

    # GPIOs einstellen
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if debug: print("GPIOs eingestellt")

    #  Init Audio und Audio-Dateien laden
    if audio:
        try:
            mixer.init()
            start_sound = mixer.Sound("medien/start.wav")
            bonus_sound = mixer.Sound("medien/bonus.wav")
            fail_sound = mixer.Sound("medien/fail.wav")
            end_sound = mixer.Sound("medien/end.wav")
            if debug: print("Audio wurde geladen")
        except:
            audio = False
            if debug: print("Audio konnte nicht geladen werden")

# funktions-schleife:
# -> warte auf input
# --> speichere die zeit für den input
# ---> ermittle die punkte
# ----> zeige einen effekt

def main():
    global running

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
                    
                    if running == False:
                        if key == "start":
                            running = True
                            get_time(key, pin)
                            #reset() -- bin hier noch auf käferjagt...
                            start()
                    else:
                        get_time(key, pin)
                        if key == "bonus":
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
    sock.send(bytes("medien/ausw:" + str("0"), "UTF-8")) # ausblenden auswertung-node
    sock.send(bytes("medien/punkte/punkte:{} | {}".format(punkte, p_multiplikator), "UTF-8"))
    if audio: mixer.Sound.play(start_sound)
    sock.send(bytes("medien/hintergrund/alpha:" + str("1"), "UTF-8")) 

    #effekt_countdown_Spielstart

def ende():
    if debug: print("ende()")
    # Statistiken fuer das Ende
    # Genaue Aufschlüsselung des extrem komplizierten und geilen *hust hust* Punktesystem
    if audio: mixer.Sound.play(end_sound)
    auswertung()
    reset()

def bonus():
    if debug: print("bonus()")
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("star.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
    # Bonus-Sound mit mixer abspielen
    if audio: mixer.Sound.play(bonus_sound) 

def fail():
    if debug: print("fail()")
    # Ein Sternchen *bling* effekt
    sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
    sock.send(bytes("medien/effekt/bildname:" + str("Pesthoernchen.png"), "UTF-8"))
    sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
    if audio: mixer.Sound.play(fail_sound)

def auswertung():
    global punkte, startzeit, zeitenListe
    if debug: print("auswertung()")
    zeit = time()
    sock.send(bytes("medien/punkte/punkte:" + str("Auswertung:"), "UTF-8"))
    sock.send(bytes("medien/hintergrund/alpha:" + str("0"), "UTF-8")) #ausblenden "See-Base"
    sock.send(bytes("medien/ausw:" + str("1"), "UTF-8")) #einblenden auswertung-node
    # Senden der Punkte
    sock.send(bytes("medien/auswertung/punkte:" + str(punkte), "UTF-8")) # Gesamtpunkte
    sock.send(bytes("medien/auswertung/zeit:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    # Sendet die Segmente:
    sock.send(bytes("medien/auswertung/segment1:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment2:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment3:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment4:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment5:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
 
def highscoreliste():
    # blendet bei laengerem idlen die aktuelle Highscoreliste ein
    pass

def punkte_setzen(aktuelle_zeit, letzte_zeit):
    # Dokumentation zum Punktesystem unter https://github.com/see-base/schwebedraht/blob/master/PUNKTE.md
    global punkte, p_multiplikator

    pin1, zeit1 = aktuelle_zeit
    pin2, zeit2 = letzte_zeit

    if pin1 in segmente["bonus"] and pin2 != pin1: # zwei mal das gleiche bonus-segment berühren wird hiermit vermieden
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

    beruehrt = 0
    for e in zeitenListe:
        if e[0] in segmente["fail"]:
            beruehrt += 1
    sock.send(bytes("medien/punkte/punkte:{} | {}".format(punkte, beruehrt), "UTF-8"))
    if debug: print("Punkte: {} | Multiplikator: {} | Berührungen: {}".format(punkte, p_multiplikator, beruehrt))

def reset():
    if debug: print("reset")
    global startzeit, zeitenListe, punkte, running , p_multiplikator
    startzeit = 0.0
    zeitenListe = []
    punkte = 0
    running = False
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
        print("\t--no-audio\t- Keine Audioausgabe")
        print("\n")
        exit()
    elif i in ["-v", "--version"]:
        print("\n{0} - {1}\n\nVersion:\t{2}\n".format(spielName, spielNameZusatz, version))
        exit()
    elif i == "--debug":
        debug = True
        print("Debug Modus")
    elif i == "--demo":
        demo = True
        print("Demo Modus")
    elif i == "--no-audio":
        audio = False
        print("Keine Audioausgabe")

if debug: print("Spiel wird vorbereitet")
setup()
if debug: print("Spiel wird gestartet")
try:
    main()
except KeyboardInterrupt:
    # diese zeile spaeter durch reset-funktion beim start ersetzen.
    sock.send(bytes("medien/punkte/punkte:0 | 1", "UTF-8"))
