#Technischer Aufbau des Spiels

Das Spiel überreicht einige Variabeln an den info-beamer. Diese werden von Python3 über `UDP` an die IP `127.0.0.1` (localhost) an Port `4444` gesendet. Von dort werden Sie vom info-beamer empfangen und verwendet.


```python

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
# Verbindung via UDP aufbauen
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("127.0.0.1", 4444))
# Variablen uebergeben
wert=42 #Wert als Variable anlegen
sock.send(bytes("medien/punkte/punkte:" + str(wert), "UTF-8")) 
# An das Child Node 'punkte' vom Haupt Node "medien" an die
# Variable "punkte" der Inhalt der Variable $wert (42) gesendet.

``` 

##Aufbau info-beamer
Der Info-Beamer ist in mehrere Nodes aufgeteilt. Jeder Node hat theoretisch die möglichkeit beliebig viele Variabeln via  UDP von dem Python Programm zu empfangen.
Dieses Setup sieht beispielsweise so aus:
```lua
gl.setup(1024, 600) --Bildschirmgroesse
punkte = 0 --Variable $punkte
util.data_mapper { --Daten via UDP Empfangen
    ["punkte"] = function(value) --an die Variable $punkte wird ein Wert uebergeben
        punkte = value  --Die Variable punkte im info-beamer hat den von Python uebergebenen Wert
    end
}

```

###medien
Der **Master Node** der gesamten Grafik. Quasi das **root** des info-beamers. Hier wird bestimmt was angezeigt werden soll und welche Child Nodes sichtbar sein sollen.

| Variabel-Name    | Wert            | Default | Funktion  |
| ---------------- |:---------------:| :-----: | ----------|
| `effekt_fade`    | 0.0 - 1.0       | `0`     | Alpha Wert des Child Node `effekt` |
| `effekt_zoom`    | *beliebige Zahl*| `0`     | Groesse des Child Node `effekt`    |

##hintergrund
Das **Child Node**, welches für den Hintergrund in unserem Spiel zuständig ist.
Dieses Child Node ist als Layer "ganz hinten" angeordnet, so dass es von allen anderen Elementen ueberdeckt wird.

##effekt
Das **Child Node**, welches fuer die Effekte zuständig ist.


| Variabel-Name    | Wert            | Default        | Funktion  |
| ---------------- |:---------------:| :------------: | ----------|
| `bildname`       | `String`        | `testbild.png` | Das Bild, welches als Effekt verwendet wird. |

##punkte
Das **Child Node**, welches für die Anzeige der Punkte verantwortlich ist!


| Variabel-Name    | Wert            | Default| Funktion  |
| ---------------- |:---------------:| :----: | ----------|
| `punkte`         | `beliebige Zahl`| `0`    | Punkte, die angezeigt werden. |

