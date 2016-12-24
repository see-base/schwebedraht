#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# sudo pip3 install pyserial
#
# Dieses kleine Script dient zum virtualisieren der WANDler
#
import socket
Quelle='127.0.0.1'
Port=5005
 
e_udp_sock = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
e_udp_sock.bind( (Quelle,Port) )
print('########Dies ist der Empfänger########'    )
print('Neue Verbindung:')
print('Quelle',Quelle)
print('Port=',Port)
 
 
 
 
def empfange():
    print("Einkommende Nachrichten:\n") 
    while 1:                                    # Endlosschleife
        data, addr = e_udp_sock.recvfrom( 1024 ) # Puffergröße: 1024 Bytes
        print(data)
 
 
empfange() #Programm wartet in einer Endlosschleife auf eingehende Nachrichten.
