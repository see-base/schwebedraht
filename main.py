#!/usr/bin/python3
# -*- coding: utf-8 -*-

#zum signale senden:
import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))

def set_image(name):
    #hier kommt noch was rein
    send_effekt_image(name)

def zoom(in_out):
    step = 0

    if in_out == 1:
        wert = 0
        while wert < 2100:
            send_effekt_zoom(wert)
            sleep(0.02)
            wert += step
            step += 3
    elif in_out == 0:
        wert = 2110
        while wert > 0:
            send_effekt_zoom(wert)
            sleep(0.02)
            wert -= step
            step += 3 

def fade_in():
    wert = 0
    for i in range(0, 50):
        send_effekt_fade(wert)
        wert = round(wert + 0.02, 2)
        sleep(0.02)

def fade_out():
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
def send_effekt_image(wert):
    sock.send(bytes("medien/effekt/bildname:" + str(wert), "UTF-8"))

set_image("testbild.png")
zoom(1)
fade_out()
set_image("star.png")
fade_in()
zoom(0)
