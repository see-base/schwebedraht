#Schnitstelle
##zwischen der Spielehardware und dem Raspberry PI

#Spielkonzept:
Das Spiel ist ein [Hei�er Draht](https://de.wikipedia.org/wiki/Hei%C3%9Fer_Draht_(Spiel) "Wikipedia"), der aus verschiedenen Segmenten besteht.
Neben den (gr��eren) Teilen, die man nicht ber�hren sollte sind (kleinere) Bonussegmente vorhanden, die einem Punkte geben, die je nach dem, wie viel Zeit man vom letzten Segment ben�tigt hat variieren. Kombinationen von Bonussegment-Ber�hungen geben nochmal mehr Punkte.
Jedes mal, wenn ein Segment ber�hrt wurde erscheint auf einem Display eine Reaktion in Form eines Videos, einer Animation und/oder einem Toneffekt.

##Hardware
Das Spiel Schwebedraht ist in mehrere Segmente eingeteilt. Die gr��eren Segmente sollte man nicht ber�hren w�hrend die kleinen Segmente Bonus-Punkte bringen k�nnen.
Jedes der Segmente ist �ber GPIO mit dem Raspberry Pi verbunden. Dadurch werden genauste Punkte ermittelt und Spielst�nde bestimmt, die dann [an den Info-Beamer weitergegeben](https://github.com/see-base/schwebedraht/blob/master/medien/Readme.md "medien/Readme.md") werden.

| Funktion       | Segment Nr. | Farbe GPIO Pin | PIN Raspberry Pi **2** |
| ---------------|:------------| :------------: | :-------:|
| Spiel starten  | 0           | Mintgruen      | `Pin 12` |
| WANDler (`Ground`)| 1        | Blau           | `Pin 14` |
| Erstes Segment | 2           | Lila           | `Pin 16` |
| Bonus #1       | 3           | Grau           | `Pin 18` |
| Zweites Segment| 4           | Weiss          | `Pin 22` |
| Bonus #2       | 5           | Schwarz        | `Pin 24` |
| Drittes Segment| 6           | Braun          | `Pin 26` |
| Bonus #3       | 7           | Rot            | `Pin 29` |
| Viertes Segment| 8           | Orange         | `Pin 31` |
| Bonus #4       | 9           | Gelb           | `Pin 33` |
| Letztes Segment| 10          | Schwarz-Gelb   | `Pin 35` |
| Spiel beenden  | 11          | Gelb-Schwarz   | `Pin 37` |
 

##Programierung:
Python3 ist eine sehr Hardware nahe Sprache und gerade am Raspberry Pi genau richtig um schnell und einfach auf die GPIOs zuzugreifen.
