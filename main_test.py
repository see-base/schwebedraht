#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Schwebedraht - Ein Spiel der see-base

# --- Bibliotheken importieren --- #

import RPi.GPIO as GPIO
from time import time, sleep


# --- Globale Variablen --- #

sock = None

segmente = {
    "start": [37]
    "bonus": [33, 29, 18]
    "malus": [35, 31, 22, 16]
    "stopp": [12]
}

startzeit = 0.0
zeiten_liste = []

punkte = 0
p_faktor = 1

running = False


# --- Helferfunktionen --- #

# Effektdaten zum info-beamer via socket schicken
def ib_send(data):
    sock.send(bytes(data, "UTF-8"))


# --- Initialisierung --- #

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for key, value in segmente.items():
        GPIO.setup(value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("GPIOs eingerichtet")

def init_socket():
	global sock

    sock = socket.socket(socket.AF_INET, socket_DGRAM)
    sock.connect(("127.0.0.1", "4444"))

    ib_send("medien/connected:True")
    ib_send("medien/punkte/punkte:#see-base")

    print("Info-Beamer Verbindung hergestellt")


# --- Hauptschleife --- #

def main():
	global running, zeiten_liste
    # Spiel initialisieren
    init_gpio()
    init_socket()

    # Spiel starten
    while True:
    
        for key, value in segmente.items():
        
            for pin in value:
            
                if not GPIO.input(pin):
                
                    if running:
                    	# Zeitstempel machen
                    	get_time(key, pin)
                    	
            			# Effekt spielen
                        effekt(key)
                        
                        sleep(0.2)
                    else:
                    
                        if key == "start":
                        	get_time(key, pin)
                            running = True


# Speichert die Pin-ID und die Zeit seit dem Spielstart in zeiten_liste
def get_time(name, pin):
    global startzeit, zeiten_liste
    
    zeit = time()

    if name == "start":
        startzeit = zeit
    
    # Zeitabstände unter einer Sekunde werden ignoriert
    if name == "start" or zeit - zeiten_liste[-1][1] > 1:
		zeiten_liste.append((pin, zeit - startzeit))
	
	print("Zeitstempel für Pin {} gesetzt: {}", pin, zeiten_liste[-1][1])

# Sendet Daten an den Info-Beamer um dort einen Effekt zu spielen.
# TODO: SFX einbauen.
def effekt(name):
	
	if name == "start":
		print("Spiele Start-Effekt"...)
		
		ib_send("medien/ausw:0")
		ib_send("medien/punkte/punkte:{} | {}".format(punkte, p_multiplikator))
		ib_send("medien/hintergrund/alpha:1")

	elif name == "malus":
		print("Spiele Malus-Effekt...")
		
		ib_send("medien/zoom_exponential:0")
		ib_send("medien/effekt/bildname:pesthoernchen.png")
		ib_send("medien/zoom:1)

	elif name == "bonus":
		print("Spiele Bonus-Effekt...")
		
		ib_send("medien/zoom_exponential:1")
		ib_send("medien/effekt/bildname:star.png")
		ib_send("medien/zoom:1")

	elif name == "stopp":
		print("Spiele Stopp-Effekt...")
		#TODO Endanimation erstellen


