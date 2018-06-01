#Schnitstelle
##zwischen der Spielehardware und dem Raspberry PI

#Spielkonzept:
Das Spiel ist ein [Heißer Draht](https://de.wikipedia.org/wiki/Hei%C3%9Fer_Draht_(Spiel) "Wikipedia"), der aus verschiedenen Segmenten besteht.
Neben den (größeren) Teilen, die man nicht berühren sollte sind (kleinere) Bonussegmente vorhanden, die einem Punkte geben, die je nach dem, wie viel Zeit man vom letzten Segment benötigt hat variieren. Kombinationen von Bonussegment-Berühungen geben nochmal mehr Punkte.
Jedes mal, wenn ein Segment berührt wurde erscheint auf einem Display eine Reaktion in Form eines Videos, einer Animation und/oder einem Toneffekt.

##Hardware
Das Spiel Schwebedraht ist in mehrere Segmente eingeteilt. Die größeren Segmente sollte man nicht berühren während die kleinen Segmente Bonus-Punkte bringen können.
Jedes der Segmente ist über GPIO mit dem Raspberry Pi verbunden. Dadurch werden genauste Punkte ermittelt und Spielstände bestimmt, die dann [an den Info-Beamer weitergegeben](https://github.com/see-base/schwebedraht/blob/master/medien/README.md "medien/README.md") werden.

| Funktion       | Segment Nr. | Farbe GPIO Pin | PIN Raspberry Pi **2** |
| ---------------|:------------| :------------: | :-------:|
| WANDler (GND)  | 0           |                | `Pin  6` |
| Start-Segment  | 1           |                | `Pin 37` |
| Malus #1       | 2           |                | `Pin 35` |
| Bonus #1       | 3           |                | `Pin 33` |
| Malus #2       | 4           |                | `Pin 31` |
| Bonus #2       | 5           |                | `Pin 29` |
| Malus #3       | 6           |                | `Pin 22` |
| Bonus #3       | 7           |                | `Pin 18` |
| Malus #4       | 8           |                | `Pin 16` |
| Stopp-Segment  | 9           |                | `Pin 12` |
