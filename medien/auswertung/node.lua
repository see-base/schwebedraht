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
segment1a = "Punkte: ??"
segment2a = "Punkte: ??"
segment3a = "Punkte: ??"
segment4a = "Punkte: ??"
segment5a = "Punkte: ??"

segment1b = "? x Beruert"
segment2b = "? x Beruert"
segment3b = "? x Beruert"
segment4b = "? x Beruert"
segment5b = "? x Beruert"

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
    ["segment1a"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment1a = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment2a"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment2a = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment3a"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment3a = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment4a"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment4a = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment5a"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment5a = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment1b"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment1b = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment2b"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment2b = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment3b"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment3b = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment4b"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment4b = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["segment5b"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        segment5b = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
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
    congress:write(210, 210, "ZEIT:", 105, 0,1,1,alpha)
    font:write(500, 210, zeit, 105, 1, 1, 0, alpha)
    
    --Anzeige Punkte:
    congress:write(10, 380, "PUNKTE:", 105, 1,1,0,alpha)
    font:write(500, 380, punkte, 105, 0,1,1,alpha)

    --Anzeige Unique Nick:
    congress:write(180, 550, "NICK:", 105, 0,1,1,alpha)
    font:write(500, 550, nick, 105, 0.5,1,0,alpha)
    font:write(60, 670, nick.." ist ein unique Name, mit dem dieser Punktestand", 32, 1,1,0,alpha)
    font:write(150, 710, "in die Highscore Liste aufgenommen wird!", 32, 1,1,0,alpha)

    --Segmentauswertung
    congress:write(5, 170, "1. SEGMENT:", 60, 0,1,1,beta)
    font:write(410, 170, segment1a, 60, 1,1,0,beta)
    font:write(710, 170, segment1b, 60, 1,1,0,beta)
    congress:write(5, 270, "2. SEGMENT:", 60, 0,1,1,beta)
    font:write(410, 270, segment2a, 60, 1,1,0,beta)   
    font:write(710, 270, segment2b, 60, 1,1,0,beta)
    congress:write(5, 370, "3. SEGMENT:", 60, 0,1,1,beta)
    font:write(410, 370, segment3a, 60, 1,1,0,beta)
    font:write(710, 370, segment3b, 60, 1,1,0,beta)
    congress:write(5, 470, "4. SEGMENT:", 60, 0,1,1,beta)
    font:write(410, 470, segment4a, 60, 1,1,0,beta)   
    font:write(710, 470, segment4b, 60, 1,1,0,beta)
    congress:write(5, 570, "5. SEGMENT:", 60, 0,1,1,beta)
    font:write(410, 570, segment5a, 60, 1,1,0,beta)
    font:write(710, 570, segment5b, 60, 1,1,0,beta)
 

end
