gl.setup(512, 130)
--Aenderungen von Funktionen bitte Dokumentieren!
local font = resource.load_font("Lato-Regular.ttf")
punkte=0 --Punkte Anzahl
width = font:width(punkte, 90)
r=1
g=0
b=0

util.data_mapper { -- Empfaengt einen Wrt von main.py
    ["punkte"] = function(value) --Funktion "punkte"
        punkte = value
        width = font:width(punkte, 90)
    end
}
util.data_mapper { -- Empfaengt einen Wrt von main.py
    ["r"] = function(value) --Funktion "punkte"
        r = value
    end
}
util.data_mapper { -- Empfaengt einen Wrt von main.py
    ["g"] = function(value) --Funktion "punkte"
        g = value
    end
}
util.data_mapper { -- Empfaengt einen Wrt von main.py
    ["b"] = function(value) --Funktion "punkte"
        b = value
    end
}


function node.render()
    gl.clear(1, 1, 1, 0.23)  
    if sys.now() > 15 then
        font:write(WIDTH / 2 - width / 2, 20, punkte, 90, r, g, b, 1)
    end
end
