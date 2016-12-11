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
# An das Child Node `punkte` wird vom Haupt Node `medien` an die
# Funktion `punkte` der Inhalt der Variable $wert (42) gesendet.

``` 

##Aufbau info-beamer
Der Info-Beamer ist in mehrere Nodes aufgeteilt. Jeder Node hat theoretisch die möglichkeit beliebig viele Variabeln via UDP von dem Python Programm zu empfangen.
Dieses Setup sieht beispielsweise so aus:
```lua
gl.setup(1024, 600) --Bildschirmgroesse
punkte = 0 --Variable $punkte
util.data_mapper { --Daten via UDP Empfangen
    ["punkte"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        punkte = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}

```

###medien
Der **Master Node** der gesamten Grafik. Quasi das **root** des info-beamers. Hier wird bestimmt was angezeigt werden soll und welche Child Nodes sichtbar sein sollen.
Das Python script kann durch das anpassen der unten stehenden Variabeln den Effekt vorbereiten und durch setzen der variabel "zoom" den Zoom-Vorgang starten.


| Variabel-Name    | Wert              | Default | Funktion                                 |
| ---------------- |:---------------:  | :-----: | ----------                               |
| `effekt_fade`    | 0.0 - 1.0         | `0`     | Alpha Wert des Child Node `effekt`       |
| `zoom`           | *positive Zahl*   | `0`     | Groesse des Child Node `effekt`          |
| `zoom_multipler` | *beliebige Zahl*  | `2`     | Geschwindigkeit beim Zoomen des Child Node `effekt`        |
| `zoom_exponential`| *beliebige Zahl* | `0`     | Exponentiale Größe des zoomenden Child Node `effekt`     |
| `zoom_fade`       | `1`, `2` oder `3`| `1`     | Verschiedene Modi um die Zeit nach dem das Child Node `effekt` ausgeblendet wird eingestellt wird  |
| `zoom_fade_option`| *positive Zahl*  | `0.05`  | Geschwindigkeit des ausblenden des Child Node `effekt`     |
| `ausw`      | 0.0 - 1.0        | `0`     | Alpha-Wert des Child-Node `auswertung` |
Leider noch nicht volständig ausgereift :-(

##hintergrund
Das **Child Node**, welches für den Hintergrund in unserem Spiel zuständig ist.
Dieses Child Node ist als Layer "ganz hinten" angeordnet, so dass es von allen anderen Elementen ueberdeckt wird.

| Variabel-Name    | Wert            | Default        | Funktion  |
| ---------------- |:---------------:| :------------: | ----------|
| `alpha`          | `0.0 - 1.0`     | `1`            | `ALPHA`-Wert des Textes: `"Schwebedraht\nEin Spiel der see-base"`. |



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

##auswertung
Das **Child Node**, welches fuer die Anzeige der ausgewerteten Punkte am Ende des Spieles zuständig ist. Aufzurufen durch berühren von dem `start`-Segment und dann dem `End`-Segment!

| Variabel-Name    | Wert            | Default   | Funktion  |
| ---------------- |:---------------:| :----:    | ----------|
| `zeit`           | `beliebige Zahl`| `none`    | Gesamt-Zeit, die angezeigt wird. |
| `punkte`         | `beliebige Zahl`| `none`    | Gesamt-Punkte, die angezeigt wird. |
| `nick`           | `string`        | `none`    | Ein Unique String, der als Nick in die Highscoreliste eingetragen wird`|

