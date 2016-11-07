# Schwebedraht
Ein Spiel der see-base

![Cyber](https://see-base.de/file/2016/03/19/IMG_20160319_161949_2.jpg "Schwebedraht")


#Spielkonzept:
Das Spiel ist ein [Heißer Draht](https://de.wikipedia.org/wiki/Hei%C3%9Fer_Draht_(Spiel) "Wikipedia"), der aus verschiedenen Segmenten besteht.
Neben den (größeren) Teilen, die man nicht berühren sollte sind (kleinere) Bonussegmente vorhanden, die einem Punkte geben, die je nach dem, wie viel Zeit man vom letzten Segment benötigt hat variieren. Kombinationen von Bonussegment-Berühungen geben nochmal mehr Punkte.
Jedes mal, wenn ein Segment berührt wurde erscheint auf einem Display eine Reaktion in Form eines Videos, einer Animation und/oder einem Toneffekt.

#Hardware:
Die Software läuft auf einem Raspberry Pi. Die einzelnen Segmente sind mit den GPIO-Pins verbunden, wodurch eine Berührung von der Software wahrgenommen werden kann.
Die Segmente selbst sind dünne Kupferrohre, an deren Innenseite ein Klingeldraht befestigt ist und nach außen führt.
An den Raspberry Pi ist ein Display und zwei kleine Lautsprecher angeschlossen.


#Grafik:
Als "Grafik Engine" kommt der [Info-Beamer](https://info-beamer.com/) zum Einsatz, der durch seinen modularen Aufbau sehr einfach anzupassen ist und dabei noch performant bleibt.

#Software:
Der Steuerungscode für das Spiel ist in **Python 3** geschrieben, die Anzeigescripts für den info-beamer in **Lua**

#Schnitstellen
[Dokumentation](https://github.com/see-base/schwebedraht/blob/master/medien/README.md "medien/README.md"). zur Schnitstelle zwischen Info-Beamer und Python3 Spiel.
[Dokumentation](https://github.com/see-base/schwebedraht/blob/master/GPIO.md "GPIO.md") zur technischen Verkabelung der GPIOs zwischen Spielehardware und Raspberry Pi.

#Kontakt:
Unser Hackerspace ist unter [see-base.de](https://see-base.de) zu finden.

Das Entwicklerteam des Schwebedraht ist unter [schwebedraht@see-base.de](mailto:schwebedraht@see-base.de) erreicbar.

#Lizenz: 
[GENERAL PUBLIC LICENSE](https://raw.githubusercontent.com/see-base/schwebedraht/master/LICENSE)
