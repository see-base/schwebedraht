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
    global audio, sock, start_sound, bonus_sound, fail_sound, end_sound
    print("\n\033[1;32;40m {0} \033[1;37;40m-\033[1;34;40m {1}\n".format(spielName, spielNameZusatz))

    #UDP-Socket einstellen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("127.0.0.1", 4444))
    if debug: print("\033[0;36;40mUDP-Socket eingestellt")

    # GPIOs einstellen
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if debug: print("\033[0;36;40mGPIOs eingestellt")

    #  Init Audio und Audio-Dateien laden
    if audio:
        try:
            mixer.init()
            start_sound = mixer.Sound("medien/start.wav")
            bonus_sound = mixer.Sound("medien/bonus.wav")
            fail_sound = mixer.Sound("medien/fail.wav")
            end_sound = mixer.Sound("medien/end.wav")
            if debug: print("\033[0;36;40mAudio wurde geladen")
        except:
            audio = False
            if debug: print("\033[0;31;40mAudio konnte nicht geladen werden")

# funktions-schleife:
# -> warte auf input
# --> speichere die zeit für den input
# ---> ermittle die punkte
# ----> zeige einen effekt

def main():
    global running

    if demo:
        print("\033[0;35;40mStarte Demo-Modus")
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
                    if debug: print("\n\033[0;37;40mPin \033[0;33;40m{}\033[0;37;40m wurde berührt | Key =\033[0;3;40m {}\033[0;37;40m".format(pin, key))
                    
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
    if debug: 
        print("auswertung()")
        print("\tPunkte: "+str(punkte)+"\n\tStartzeit: "+str(startzeit)+"\n\tzeitenListe:\n"+str(zeitenListe)+"\n\n")
    zeit = time()
    sock.send(bytes("medien/punkte/punkte:" + str("Auswertung:"), "UTF-8"))
    sock.send(bytes("medien/hintergrund/alpha:" + str("0"), "UTF-8")) #ausblenden "See-Base"
    sock.send(bytes("medien/ausw:" + str("1"), "UTF-8")) #einblenden auswertung-node
    # Senden der Punkte
    sock.send(bytes("medien/auswertung/punkte:" + str(punkte), "UTF-8")) # Gesamtpunkte
    sock.send(bytes("medien/auswertung/zeit:" + str(zeit - startzeit), "UTF-8")) # Gesamtzeit
    # Die einzelnen Segmente:
    for liste in zeitenListe:
        if debug: print("Auswertung der zeitenListe:")
        gpio, beruehrung = liste

    #
    # DRAFT:
    #


    # S. = anfang, ende, ges.zeit, beruehrt
    seg1 = [False, False, False, False]
    seg2 = [False, False, False, False]
    seg3 = [False, False, False, False]
    seg4 = [False, False, False, False]
    seg5 = [False, False, False, False]
    for liste in zeitenListe:
        print(str(liste))
        gpio, beruehrung = liste
        zustand = False
        for a, b in segmente.items():
            if gpio in b: zustand = a
        print(str(zustand))
        print(len(segmente["bonus"]))
    
        # kann man mal vernuenftig, dynamisch und cool machen...
        if zustand == "fail":
            if gpio == segmente["fail"][0]: seg1[3] += 1
            if gpio == segmente["fail"][1]: seg2[3] += 1       
            if gpio == segmente["fail"][2]: seg3[3] += 1
            if gpio == segmente["fail"][3]: seg4[3] += 1
            if gpio == segmente["fail"][4]: seg5[3] += 1


        # Segment-Anfang ermitteln:
        if zustand == "start":
            if seg1[0] == False:        
                seg1[0] = beruehrung
            else:
                if seg1[0] < beruehrung: seg1[0] = beruehrung
    
        if gpio == segmente["bonus"][0]:
            if seg2[0] == False:        
                seg2[0] = beruehrung
            else:
                if seg2[0] < beruehrung: seg2[0] = beruehrung
    
        if gpio == segmente["bonus"][1]:
            if seg3[0] == False:        
                seg3[0] = beruehrung
            else:
                if seg3[0] < beruehrung: seg3[0] = beruehrung
    
        if gpio == segmente["bonus"][2]:
            if seg4[0] == False:        
                seg4[0] = beruehrung
            else:
                if seg4[0] < beruehrung: seg4[0] = beruehrung

        if gpio == segmente["bonus"][3]:
            if seg5[0] == False:        
                seg5[0] = beruehrung
            else:
                if seg5[0] < beruehrung: seg5[0] = beruehrung

        # Segment-Ende ermitteln:
    

        if gpio == segmente["bonus"][0]:
            if seg1[1] == False:        
                seg1[1] = beruehrung
            else:
                if seg1[1] > beruehrung: seg1[1] = beruehrung
    
        if gpio == segmente["bonus"][1]:
            if seg2[1] == False:        
                seg2[1] = beruehrung
            else:
                if seg2[1] > beruehrung: seg2[1] = beruehrung
    
    
        if gpio == segmente["bonus"][2]:
            if seg3[1] == False:        
                seg3[1] = beruehrung
            else:
                if seg3[1] > beruehrung: seg3[1] = beruehrung
    

        if gpio == segmente["bonus"][3]:
            if seg4[1] == False:        
                seg4[1] = beruehrung
            else:
                if seg4[1] > beruehrung: seg4[1] = beruehrung


        if gpio == segmente["bonus"][0]:
            if seg1[1] == False:        
                seg1[1] = beruehrung
            else:
                if seg1[1] > beruehrung: seg1[1] = beruehrung


        if zustand == "ende":
            if seg5[1] == False:        
                seg5[1] = beruehrung
            else:
                if seg5[1] > beruehrung: seg5[1] = beruehrung


        # Punkte zahlen:
        seg1[2] = seg1[1] - seg1[0]

        
    sock.send(bytes("medien/auswertung/segment1:" + str(seg1), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment2:" + str(seg2), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment3:" + str(seg3), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment4:" + str(seg4), "UTF-8")) # Gesamtzeit
    sock.send(bytes("medien/auswertung/segment5:" + str(seg5), "UTF-8")) # Gesamtzeit
 
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
        print("\n\033[1;32;40m {0} \033[1;37;40m-\033[1;34;40m {1}\n".format(spielName, spielNameZusatz))
        print("\033[0;37;40m Quelle: https://github.com/see-base/schwebedraht\n\n")
        print("\033[0;33;40mMoegliche Befehle:\n\033[0;33;40m\t --help \t\033[0;37;40m-\033[0;36;40m Zeigt diese Hilfe an")
        print("\t\033[0;33;40m --version\t\033[0;37;40m-\033[0;36;40m Zeigt die Version des Spieles")
        print("\t\033[0;33;40m --debug\t\033[0;37;40m-\033[0;36;40m Debug Modus...")
        print("\t\033[0;33;40m --demo  \t\033[0;37;40m-\033[0;36;40m Demo Modus")
        print("\t\033[0;33;40m --no-audio\t\033[0;37;40m-\033[0;36;40m Keine Audioausgabe")
        print("\n\033[0;37;40m")
        exit()
    elif i in ["-v", "--version"]:
        print("\n\033[1;32;40m {0} \033[1;37;40m-\033[1;34;40m {1}\n\033[1;36;40m\n Version:\t{2}\n".format(spielName, spielNameZusatz, version))
        exit()
    elif i == "--debug":
        debug = True
        print("\033[0;36;40mDebug Modus")
    elif i == "--demo":
        demo = True
        print("\033[0;36;40mDemo Modus")
    elif i == "--no-audio":
        audio = False
        print("\033[0;36;40mKeine Audioausgabe")

if debug: print("\033[0;36;40mSpiel wird vorbereitet")
setup()
if debug: print("\033[0;36;40mSpiel wird gestartet")
try:
    main()
except KeyboardInterrupt:
    # diese zeile spaeter durch reset-funktion beim start ersetzen.
    sock.send(bytes("medien/punkte/punkte:0 | 1", "UTF-8"))
