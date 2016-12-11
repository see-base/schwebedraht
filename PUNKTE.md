##Das Punktesystem beim Schwebedraht:

Das tolle an diesem Spiel ist unter anderem, dass man die moeglichkeit hat Punkte zu erzielen kann und diese auch in einer Highscore-Liste auftauchen koennten.
Doch bevor man die Punkte erzielt, muessen diese erst einmal verdient werden. Dies geschieht durch BerÃuehren der Bonus segmente in bestimmten Zeiten und ein wenig Glueck!

#Spielen
Mit dem Beruehren des Start-Segments aktiviert man das Spiel und es koennen Punkte verdient werden. Beim Erhalten von `PUNKTEN` ertÃnt ein Sound und es erscheint ein allgemein eher als Belohnung wazunehmendes Symbol auf dem Display. Beispielsweise ein Stern.

##get_time:
**Technisch** funktioniert das so, dass *irgendwann* die Funktion `get_time` die Variablen `name` und `pin` bekommt.
`name` = Die Funktion des Segmentes, das man soeben beruehrt hat. Zum Beispiel `start` oder `bonus`!
`pin` = Die GPIO Pin Nummer, die tatsaechlich beruehrt wurde. Siehe auch unter [GPIO.md](https://github.com/see-base/schwebedraht/blob/master/GPIO.md)

Dann wird die aktuelle Zeit erfasst. Wenn wir nicht beim `start`-Segment sind, dann wird es jetzt spannend!
Zuerst fuegen wir in die globale Liste `zeitenListe` die Pin-Nummer und die Spielzeit *(Also die aktuelle Zeit minus die Startzeit dieser Spielrunde)* der Liste hinzu.

Ist nun die aktuelle Zeit mehr als 1 Sekunde von der zuvor in die Liste eingetragenen Zeit entfernt, so uebergeben wir den aktuellen Eintrag aus der `zeitenListe` und den vorherigen Eintrag der Funktion `punkte_setzen`
```python

def get_time(name, pin):
    zeit = time()
    if name == "start":
    startzeit = zeit
        zeitenListe.append((pin, zeit - startzeit))
    else:
        zeitenListe.append((pin, zeit - startzeit))
        if zeitenListe[-1][1] - zeitenListe[-2][1] > 1:
            punkte_setzen(zeitenListe[-1], zeitenListe[-2])
        else: zeitenListe.pop()

```

##punkte_setzen:

In dieser Funktion werden als erstes die Eintraege aus der `zeitenListe` wieder auf einzelne variablen aufgeteilt. AuÃŸerdem werden die Globalen variablen `punkte` Und der punkte Multiplikator verwendet.

```python

def punkte_setzen(aktuelle_zeit, letzte_zeit):
    global punkte, p_multiplikator
    
    pin1, zeit1 = aktuelle_zeit
    pin2, zeit2 = letzte_zeit
    
```
Ist die beruehrte Stelle eine Bonus-Stelle, dann wird als erstes geprueft, ob die zuvor beruehrte Stelle aus dem selben Segment ist, also die selbe `pin`-Nummer hat.
Ist dem nicht der Fall, koennen folgende Sachen passieren:
 - Hat man diese Bonusstelle innerhalb von 5 Sekunden erreicht, verdoppelt sich der Multiplikator.
 - Hat man diese Bonusstelle innerhalb von 10 Sekunden erreicht, so erhoeht sich der Multiplikator um `1`!
 - Hat man aber laenger als 15 Sekunden gebraucht, so geht der Multiplikator um 1 Zurueck!

Schliesslich werden die Punkte um eine zufaellige Zahl zwischen 10 und 50 erzeugt und mit dem Multiplikator multipliziert. Und dann auch dem Gesamt-Punktestand hinzugefuegt.

```python

    if pin1 in segmente["bonus"] and pin2 != pin1: 
    # zwei mal das gleiche bonus-segment beruehren wird hiermit vermieden
        if zeit1 - zeit2 <= 5:   # m. verdoppelt sich bis 5 sek
            p_multiplikator *= 2
        elif zeit1 - zeit2 <= 10: # m. erhoeht sich um 1 bis 10 sek
            p_multiplikator += 1
        elif zeit1 - zeit2 >= 15: # m. wird zurueckgesetzt ab 15 sek
            p_multiplikator = 1
            
        punkte += randint(10, 50) * p_multiplikator # punke setzen
        
```
Falls man allerdings ein Segment des Types `fail` beruehrt haben sollte, so wird der Multiplikator halbiert, solange dieser mehr wie 1 betraegt:

```python

    elif pin1 in segmente["fail"]:
        if p_multiplikator > 1: # bei beruehrung wird m. halbiert
            p_multiplikator = math.ceil(p_multiplikator / 2)

```
Zu guter letzt wird noch gezahlt, wie oft insgesamt ein `fail`-Segment beruehrt worden ist:

```python

    beruehrt = 0
    for e in zeitenListe: 
        if e[0] in segmente["fail"]:
            beruehrt += 1
            
```




