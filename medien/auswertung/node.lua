gl.setup(1024, 750)
node.set_flag "slow_gc"
node.gc()
--Aenderungen von Funktionen bitte Dokumentieren!

--Hintergrund foo
local congress = resource.load_font("33c3.ttf")
local font = resource.load_font("Lato-Regular.ttf")
--Gesamt
zeit = "none"
punkte = "none"
nick = "none"
time = sys.now()
alpha = 1
--Segmente
beta = 0
segment1 = "Punkte: ??, Zeit: ??"
segment2 = "Punkte: ??, Zeit: ??"
segment3 = "Punkte: ??, Zeit: ??"
segment4 = "Punkte: ??, Zeit: ??"
segment5 = "Punkte: ??, Zeit: ??"

util.data_mapper { --Daten via UDP Empfangen
    ["zeit"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        zeit = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
        time = sys.now()
        alpha = 1
        beta = 0
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["punkte"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        punkte = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
        time = sys.now()
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["nick"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        nick = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
        time = sys.now()
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment1"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment1 = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment2"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment2 = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment3"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment3 = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment4"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment4 = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment5"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment5 = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}

--Rendere den Infobeamer   
function node.render()
    sysnow = sys.now()
    if (sysnow > (time + 7.3)) then
        alpha = 0
        beta = 1
    end
    --Gesampauswertung:
    --Anzeige Zeit:
    congress:write(170, 210, "Zeit:", 105, 0,1,1,alpha)
    font:write(450, 210, zeit, 105, 1, 1, 0, alpha)
    
    --Anzeige Punkte:
    congress:write(30, 380, "Punkte:", 105, 1,1,0,alpha)
    font:write(450, 380, punkte, 105, 0,1,1,alpha)

    --Anzeige Unique Nick:
    congress:write(160, 550, "Nick:", 105, 0,1,1,alpha)
    font:write(450, 550, nick, 105, 0.5,1,0,alpha)
    font:write(60, 670, nick.." ist ein unique Name, mit dem dieser Punktestand", 32, 1,1,0,alpha)
    font:write(150, 710, "in die Highscore Liste aufgenommen wird!", 32, 1,1,0,alpha)

    --Segmentauswertung
    congress:write(40, 170, "1. Segment:", 60, 0,1,1,beta)
    font:write(400, 170, segment1, 60, 1,1,0,beta)
    congress:write(40, 270, "2. Segment:", 60, 0,1,1,beta)
    font:write(400, 270, segment2, 60, 1,1,0,beta)   
    congress:write(40, 370, "3. Segment:", 60, 0,1,1,beta)
    font:write(400, 370, segment3, 60, 1,1,0,beta)
    congress:write(40, 470, "4. Segment:", 60, 0,1,1,beta)
    font:write(400, 470, segment4, 60, 1,1,0,beta)   
    congress:write(40, 570, "5. Segment:", 60, 0,1,1,beta)
    font:write(400, 570, segment5, 60, 1,1,0,beta)
 

end
