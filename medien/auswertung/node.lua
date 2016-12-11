gl.setup(1024, 750)
node.set_flag "slow_gc"
node.gc()
--Aenderungen von Funktionen bitte Dokumentieren!

--Hintergrund foo
local congress = resource.load_font("33c3.ttf")
local font = resource.load_font("Lato-Regular.ttf")
zeit = "none"
punkte = "none"
nick = "none"
util.data_mapper { --Daten via UDP Empfangen
    ["zeit"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        zeit = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["punkte"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        punkte = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}
util.data_mapper { --Daten via UDP Empfangen
    ["nick"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        nick = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}

--Rendere den Infobeamer   
function node.render()
    --Anzeige Zeit:
    congress:write(170, 210, "Zeit:", 105, 0,1,1,1)
    font:write(450, 210, zeit, 105, 1, 1, 0, 1)
    
    --Anzeige Punkte:
    congress:write(30, 380, "Punkte:", 105, 1,1,0,1)
    font:write(450, 380, punkte, 105, 0,1,1,1)

    --Anzeige Unique Nick:
    congress:write(160, 550, "Nick:", 105, 0,1,1,1)
    font:write(450, 550, nick, 105, 0.5,1,0,1)
    font:write(60, 670, nick.." ist ein unique Name, mit dem dieser Punktestand", 32, 1,1,0,1)
    font:write(150, 710, "in die Highscore Liste aufgenommen wird!", 32, 1,1,0,1)
end
