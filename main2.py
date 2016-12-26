#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#

from pygame import mixer
import socket
import random, serial

vfx = { "fail" : ["Pesthoernchen.png"],
                    "start" : [],
                    "ziel" : ["star.png"]
    }
sfx = [] # 0 = fail, 1 = start, 2 = bonus, 3 = ende

#init UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

#init serial

ser = serial.Serial("/dev/ttyUSB0", 115200)

#init audio-system
try:
	mixer.init()
	sfx.append(mixer.Sound("medien/fail.wav"))
	sfx.append(mixer.Sound("medien/start.wav"))
	sfx.append(mixer.Sound("medien/bonus.wav"))
	sfx.append(mixer.Sound("medien/end.wav"))

except:
    pass

def main():
    while True:
        ID, INT, BAT, F = serial_decoder()

        if F in range(90, 110): # frequenz um 100 khz, mit +-10 khz toleranz
            aktion(1) #uebergibt das segment als zahl
        elif F in range(190, 210):
            aktion(2)
        elif F in range(290, 310):
            aktion(3)
        elif F in range(390, 410):
            aktion(4)
        else:
            aktion(0)

def serial_decoder():
    input_string = ser.readline()
    input_split = input_string.decode().split(";")

    return (int(input_split[0][3:]),
        int(input_split[1][4:]),
        int(input_split[2][4:]),
        int(input_split[3][2:]))

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
	if vfx_index == 0:
		sock.send(bytes("medien/zoom_exponential:" + str(0), "UTF-8"))
		sock.send(bytes("medien/effekt/bildname:" + random.choice(vfx["fail"]), "UTF-8"))
		sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
	elif vfx_index == 1:
		sock.send(bytes("medien/ausw:" + str("0"), "UTF-8")) # ausblenden auswertung-node
		sock.send(bytes("medien/punkte/punkte:{}".format("00:00"), "UTF-8")) #spaeter: aktuelle zeit
		sock.send(bytes("medien/hintergrund/alpha:" + str("1"), "UTF-8"))
	elif vfx_index == 2:
		sock.send(bytes("medien/zoom_exponential:" + str(1), "UTF-8"))
		sock.send(bytes("medien/effekt/bildname:" + random.choice(vfx["ziel"]), "UTF-8"))
		sock.send(bytes("medien/zoom:" + str(1), "UTF-8"))
	elif vfx_index == 3:
		sock.send(bytes("medien/punkte/punkte:" + str("Auswertung:"), "UTF-8"))
		sock.send(bytes("medien/hintergrund/alpha:" + str("0"), "UTF-8")) #ausblenden "See-Base"
		sock.send(bytes("medien/ausw:" + str("1"), "UTF-8")) #einblenden auswertung-node

def audio_effekt(sfx_index):
	if len(sfx) > 0:
		mixer.Sound.play(sfx[sfx_index])

main()
