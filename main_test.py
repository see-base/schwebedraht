#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Schwebedraht - Ein Spiel der see-base

# --- Bibliotheken importieren --- #

import RPi.GPIO as GPIO
import socket
from time import time, sleep
from random import randint, choice
#from pygame import mixer

# --- Globale Variablen --- #

sock = None # UDP-Socket
#mixer = None #Pygame Audio Mixer

segmente = {
    "start": [37],
    "bonus": [33, 29, 18],
    "malus": [35, 31, 22, 16],
    "stopp": [12]
}

startzeit = 0.0
zeiten_liste = []

punkte = 0
p_faktor = 1
beruehrt = 0

highscore_list = []

running = False


# --- Helferfunktionen --- #

# Effektdaten zum info-beamer via socket schicken
def ib_send(data):
    sock.send(bytes(data, "UTF-8"))

# Mit Pygame-Mixer Sound spielen
#def mixer_play(data):
#    mixer.Sound.play(mixer.Sound(data))

# --- Initialisierung --- #

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("GPIOs eingerichtet")

def init_socket():
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("127.0.0.1", 4444))

    ib_send("medien/connected:True")
    ib_send("medien/punkte/punkte:#see-base")

    print("Info-Beamer Verbindung hergestellt")

#def init_audio():
#   global mixer
#
#   mixer.init()
#
#   print("Audiosystem eingerichtet")

def reset_game():
    global startzeit, zeiten_liste, punkte, p_faktor, beruehrt, running

    startzeit = 0.0
    zeiten_liste = []

    punkte = 0
    p_faktor = 1
    beruehrt = 0

    running = False
    
    print("Spielwerte zurückgesetzt")


# --- Hauptschleife --- #

def main():
    global running, zeiten_liste

# Spiel initialisieren
    init_gpio()
    init_socket()
    #init_audio()

    simulator()

    # Spiel starten
    while True:

        for key, value in segmente.items():

            for pin in value:

                if not GPIO.input(pin):
                    print("Pin {} wurde berührt | Key = {} | Das Spiel läuft{}."
                        .format(pin, key, "" if running else " nicht"))

                    if running:
                        # Zeitstempel machen
                        set_time(key, pin)

                        # Punkte ermitteln
                        set_score()

                        # Effekt erzeugen
                        #if audio: play_sfx(key)
                        play_vfx(key)

                        if key == "stopp":
                            reset_game()
                        # TODO: Endsequenz (Auswertung, Rangliste, etc.)

                        sleep(0.2)
                    else:

                        if key == "start":
                            reset_game()
                            
                            running = True
                            set_time(key, pin)
                            play_vfx(key)


# Simulierte GPIO-Pin Eingabe mit der Tastatur für Debuggingzwecke.
def simulator():
    global running, zeiten_liste

    # Simulation
    while True:

        x = int(input())
        
        for key, pins in segmente.items():

            if x in pins:

                if running:
                    set_time(key, x)
                    set_score()
                    play_vfx(key)

                    if key == "stopp":
                        reset_game()
                        sleep(2.0)
                else:

                    if key == "start":
                        reset_game()
                        running = True
                        set_time(key, x)
                        play_vfx(key)


# --- Funktionen für die Spiellogik --- #

# Speichert die Pin-ID und den Zeitpunkt der Berührung seit dem Spielstart in
# zeiten_liste
def set_time(name, pin):
    global startzeit, zeiten_liste
    
    zeit = time()

    if name == "start":
        startzeit = zeit

    # Zeitabstände unter einer Sekunde werden ignoriert
    if name == "start" or zeit - zeiten_liste[-1][1] > 1:
        zeiten_liste.append((pin, zeit - startzeit))

    print("Zeitstempel für Pin {} gesetzt: {}".format(pin, zeiten_liste[-1][1]))

def set_score():
    global beruehrt, punkte, p_faktor, zeiten_liste

    neue_punkte = 0
    delta = "-"

    pin1, zeit1 = zeiten_liste[-1] # Aktueller Zeitstempel
    pin2, zeit2 = zeiten_liste[-2] # Vorheriger Zeitstempel

    # Wurde ein Bonussegment berührt, werden in abhängigkeit der Benötigten Zeit
    # Punkte vergeben. Man kann die gleiche Bonusstelle nicht zwei mal in Folge
    # berühren. (mehr in PUNKTE.md)
    if pin1 in segmente["bonus"] and pin1 != pin2:

        delta = zeit1 - zeit2

        if delta <= 5: # Zeitdelta bis 5 Sekunden: Faktor verdoppelt sich
            p_faktor *= 2
        elif delta <= 10: # Zeitdelta bis 10 Sekunden: Faktor um 1 erhöht
            p_faktor += 1
        elif delta >= 25: # Zeitdelta ab 25 Sekunden: Faktor wird zurück gesetzt
            p_faktor = 1

        neue_punkte = randint(10, 50) * p_faktor
        punkte += neue_punkte

    # Wird ein Malussegment berührt, wird der Faktor halbiert
    elif pin1 in segmente["malus"]:
        if p_faktor > 1:
            p_faktor = p_faktor // 2
        beruehrt += 1

    print("Punkte: {} (+{}), Zeitdelta: {}, Punkte-Faktor: {}, Berührungen: {}"
        .format(punkte, neue_punkte, delta, p_faktor, beruehrt))

    # TODO: Spezialzüge wie:
    #       - nur Bonussegmente berührt
    #       - von hinten nach vorne gespielt (start-3-2-1-ziel)
    #       etc. belohnen!

    ib_send("medien/punkte/punkte:{} | {}".format(punkte, beruehrt))


# Spielt den jeweiligen Soundeffekt über Pygame Mixer ab
#def play_sfx(name):
#    if name == "start":
#        print("Spiele Start-Sound")
#
#        mixer_play("medien/start.wav")
#
#    elif name == "malus":
#        print("Spiele Malus-Sound")
#
#        mixer_play("medien/fail.wav")
#
#    elif name == "bonus":
#        print("Spiele Bonus-Sound")
#
#        mixer_play("medien/bonus.wav")
#
#    elif name == "stopp":
#        print("Spiele Stopp-Sound")
#
#        mixer_play("medien/end.wav")

# Sendet Daten an den Info-Beamer um dort einen Effekt zu spielen
def play_vfx(name):

    if name == "start":
        print("Zeige Start-Animation")

        ib_send("medien/ausw:0")
        #ib_send("medien/highscore:0")
        ib_send("medien/punkte/punkte:{} | {}".format(punkte, beruehrt))
        ib_send("medien/hintergrund/alpha:1")
        #TODO: Start Animation

    elif name == "malus":
        print("Zeige Malus-Animation")

        ib_send("medien/zoom_exponential:0")
        ib_send("medien/effekt/bildname:pesthoernchen.png")
        ib_send("medien/zoom:1")

    elif name == "bonus":
        print("Zeige Bonus-Animation")

        ib_send("medien/zoom_exponential:1")
        ib_send("medien/effekt/bildname:star.png")
        ib_send("medien/zoom:1")

    elif name == "stopp":
        print("Zeige Stopp-Animation")
        
        gen_highscore_list()
        
        # TODO: Highscore-Node im Info-Beamer erstellen
        #ib_send("medien/highscore:1")
        
        #for i, (p, n) in enumerate(highscore_list):
        #    ib_send("medien/highscore/top{}:{}  -  {}".format(i, n, p))

# Zufälligen Namen für die Highscoreliste erstellen
def unique_nick():
    vokal = ["a", "e", "i", "o", "u"]
    nick = ( chr(randint(97, 122)).upper()
        + choice(vokal)
        + chr(randint(97, 122))
        + choice(vokal)
        + chr(randint(97, 122))
        + choice(vokal) )

    print("Unique Nick generiert: {}".format(nick))

    return nick

# Füge die Punkte der Highscoreliste hinzu.
def gen_highscore_list():
    global highscore_list, punkte

    nick = unique_nick()

    highscore_list.append((punkte, nick)) # füge neues Nick/Punkte-Paar der Liste hinzu
    highscore_list.sort() # sortiere die Liste
    highscore_list = highscore_list[::-1] # kehre die reihenfolge um

    print("{} hat {} Punkte erreicht."
        .format(nick, punkte))

    # Nur die 7 besten bleiben bestehen.
    if len(highscore_list) > 7:
        highscore_list.pop()

        print("{} hat hat es nicht in die Highscoreliste geschafft.".format(nick))

    for i, (p, n) in enumerate(highscore_list):
        print("Platz {}: {} mit {} Punkten.".format(i + 1, n, p))

# TODO: Kommandozeilenargumente auswerten (Hilfe, Version) und verschiedene Modi
#       (Ohne Ton, Verbose, Demo, Simulation ohne Raspi) einbauen.


# Programm starten
try:
    print("Spiel wird gestartet...")
    main()
# Bei Unterbrechung den Info-Beamer zurücksetzen 
except KeyboardInterrupt:
    ib_send("medien/punkte/punkte:#see-base")
    ib_send("medien/connected:False")
    ib_send("medien/hintergrund/alpha:1")
    ib_send("medien/ausw:0")
