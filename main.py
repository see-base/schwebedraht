#!/usr/bin/python3
# -*- coding: utf-8 -*-

#zum signale senden:
import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

def main():

    for p in range(0, 10000):
        send_punkte(p)
        sleep(0.01)

        if p % 1000 == 0:
            zoomin()
            fadeout()

def zoomin():

    wert = 0
    step = 1

    while wert < 2117: #ausprobierter-wert
        send_effekt_zoom(wert)
        sleep(0.02)
        wert += step
        step += 3

def fadeout():

    wert = 1
    for i in range(0, 50):
        send_effekt_fade(wert)
        wert = round(wert - 0.02, 2)
        sleep(0.02)

def send_punkte(wert):
    sock.send(bytes("medien/punkte/punkte:" + str(wert), "UTF-8"))

def send_effekt_zoom(wert):
    sock.send(bytes("medien/effekt_zoom:" + str(wert), "UTF-8"))

def send_effekt_fade(wert):
    sock.send(bytes("medien/effekt_fade:" + str(wert), "UTF-8"))

main()
