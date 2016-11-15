#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Schwebedraht - ein Spiel der see-base
#
# fuer die komandozeilenargumente
from sys import argv

# Globale Variabeln:
spielName = "Schwebedraht"
spielNameZusatz = "Ein Spiel der see-base"
version = "0.1"

# komandozeilenargumente
for i in argv:
    if ((i == "--help") or (i == "-h") or (i == "/h") or (i == "/help") or (i == "?") or (i == "h")):
        print("\n"+spielName+" - "+spielNameZusatz+"\n")
        print("Quelle: https://github.com/see-base/schwebedraht\n\n")
        print("Moegliche Befehle:\n\t--help\t- Zeigt diese Hilfe an")
        print("\t-v\t- Zeigt die Version des Spieles")
        print("\t...")
        print("\n")
        exit(0)
    print("\n"+spielName+" - "+spielNameZusatz+"\n\nVersion:\t"+version+"\n") if i == "-v" else 0
    exit(0) if i == "-v" else 0

