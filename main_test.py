#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Schwebedraht - Ein Spiel der see-base

import RPi.GPIO as GPIO # Raspi GPIO-Bibliothek
from pygame import mixer
from time import sleep

# Helferfunktionen

# effektdaten zum info-beamer via socket schicken
def ib_send(sock, data):
    sock.send(bytes(data, "UTF-8"))


# Initialisierung

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("GPIOs eingerichtet")

def init_socket():
    sock = socket.socket(socket.AF_INET, socket_DGRAM)
    sock.connect(("127.0.0.1", "4444"))

    ib_send(sock, "medien/connected:True")
    ib_send(sock, "medien/punkte/punkte:#see-base")

    print("Info-Beamer Verbindung hergestellt")


def main():
    # Spiel-Variablen einrichten
    segmente = {
        "start": [37]
        "bonus": [33, 29, 18]
        "malus": [35, 31, 22, 16]
        "stopp": [12]
    }

    running = False

    # Spiel initialisieren
    init_gpio()
    init_socket()

    # Spiel starten
    while True:
        for key, value in segmente:
            for pin in value:
                if not GPIO.input(pin):
                    if running:
                        if key == "malus":
                            pass
                        elif key == "bonus":
                            pass
                        elif key == "stopp":
                            pass
                        sleep(0.2)

                    else:
                        if key == "start":
                            running = True







