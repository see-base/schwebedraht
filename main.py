#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#  Supersize Edition
#
from pygame import mixer
import socket
import random
from serial import Serial
from sys import argv

debug = False
serial = True

vfx = { "fail" : ["pesthorn.png"],
                    "start" : [],
                    "ziel" : ["star.png"]
    }
sfx = [] # 0 = fail, 1 = start, 2 = bonus, 3 = ende
ID, INT, BAT, F = (None, None, None, None)

#init UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

#init serial
if debug: print ("Init serial")

ser = Serial("/dev/ttyUSB0", 115200)

Quelle='127.0.0.1'
Port=5005
e_udp_sock = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
e_udp_sock.bind( (Quelle,Port) ) 

#init audio-system
try:
	mixer.init()
	sfx.append(mixer.Sound("medien/fail.wav"))
	sfx.append(mixer.Sound("medien/start.wav"))
	sfx.append(mixer.Sound("medien/bonus.wav"))
	sfx.append(mixer.Sound("medien/end.wav"))

except:
    pass

spieler_liste = [(42, "green"), (23, "red"), (66, "blue"), (34, "yellow")]

def main():
    global ID, INT, BAT, F
    while True:
        ID, INT, BAT, F = serial_decoder()
        if debug: print("ID:{};INT:{};BAT:{};F:{}".format(ID, INT, BAT, F))
        if ID and INT and BAT and F:
        
            if INT == 2: # wenn draht beruehrt wurde
                if F in range(90, 110): # frequenz um 100 khz, mit +-10 khz toleranz
                    aktion(1) #uebergibt das segment als zahl
                elif F in range(190, 210):
                    aktion(2)
                elif F in range(290, 310):
                    aktion(3)
                elif F in range(490, 510):
                    aktion(4)
                else:
                    aktion(0)

def serial_decoder():
    if debug: print("RAW-Input: ")
    input_sting = ""
    if serial:
        input_string = ser.readline()
    else:
        input_sting = e_udp_sock.recvfrom( 1024 ) # Puffergröße: 1024 Bytes 
    if debug: print (input_string)
    if len(input_string) >= 28:
        input_split = input_string.decode().split(";")

        return (int(input_split[0][3:]),
            int(input_split[1][4:]),
            int(input_split[2][4:]),
            int(input_split[3][2:]))
    else:
        if debug: print("Fehlerhafter Input")
        return (None, None, None, None)
    if debug: print(input_string)

def aktion(segment):
    effekt(segment)

def effekt(segment):
    if segment == 1:
        visueller_effekt(1)
        audio_effekt(1)
    elif segment == 2:
        visueller_effekt(2)
        audio_effekt(2)
    elif segment == 3:
        visueller_effekt(2)
        audio_effekt(2)
    elif segment == 4:
        visueller_effekt(3)
        audio_effekt(3)
    else:
        visueller_effekt(0)
        audio_effekt(0)

def visueller_effekt(vfx_index):
    if debug: print("ID: " + str(ID))
    prefix = False
    if ID ==  spieler_liste[0][0]:
        if debug: print("Spieler 1")
        prefix = spieler_liste[0][1] + "-"
    elif ID == spieler_liste[1][0]:
        prefix = spieler_liste[1][1] + "-"
        if debug: print("Spieler 2")
    elif ID == spieler_liste[2][0]:
        prefix = spieler_liste[2][1] + "-"
        if debug: print("Spieler 3")
    else:
        prefix = spieler_liste[3][1] + "-"
        if debug: print("Spieler 4" + str(spieler_liste[3][0]))

    try: 
        if debug: print("Prefix: "+prefix)
        if vfx_index == 0:
            sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
            sock.send(bytes("medien/effekt/bildname:" + prefix + random.choice(vfx["fail"]), "UTF-8"))
            sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
        elif vfx_index == 1:
            sock.send(bytes("medien/ausw:" + str("0"), "UTF-8")) # ausblenden auswertung-node
            sock.send(bytes("medien/punkte/punkte:{}".format("00:00"), "UTF-8")) #spaeter: aktuelle zeit
            sock.send(bytes("medien/hintergrund/alpha:" + str("1"), "UTF-8"))
        elif vfx_index == 2:
            sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
            sock.send(bytes("medien/effekt/bildname:" + prefix + random.choice(vfx["ziel"]), "UTF-8"))
            sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
        elif vfx_index == 3:
            sock.send(bytes("medien/punkte/punkte:" + str("Auswertung:"), "UTF-8"))
            sock.send(bytes("medien/hintergrund/alpha:" + str("0"), "UTF-8")) #ausblenden "See-Base"
            sock.send(bytes("medien/ausw:" + str("1"), "UTF-8")) #einblenden auswertung-node
        elif vfx_index == 5:
            # Spiel auf "disconnected" stellen!
            sock.send(bytes("medien/punkte/punkte:#see-base", "UTF-8"))
            sock.send(bytes("medien/connected:False", "UTF-8"))
            sock.send(bytes("medien/hintergrund/alpha:" + str("1"), "UTF-8")) #einblenden "See-Base"
            sock.send(bytes("medien/ausw:" + str("0"), "UTF-8")) #ausblenden auswertung-node

    except:
        if debug: print("prefix not defined")
def audio_effekt(sfx_index):
	if len(sfx) > 0:
		mixer.Sound.play(sfx[sfx_index])

for i in argv:
    if i in ["-h", "--help"]:
        print("--debug fuer debugging")
        print("--udp fuer UDP Simulationsmodus")
        exit()
    if i == "--debug":
        debug = True
        print("Debug Modus")
    if i == "--udp":
        serial = False

try:
    main()
except KeyboardInterrupt:
    visueller_effekt(5)
