gl.setup(1024, 600)

--Hintergrund foo

local font = resource.load_font("Lato-Regular.ttf")
hintergrund_child = "hintergrund" -- Node fuer Hintergrund Bild/Animation/Wasauchimmer
effekt_child = "effekt" -- Node fuer Effekte bei einem Event
punkte_child = "punkte" -- Node fuer die Punkteanzeige

effekt_sichtbar = 0

width_effekt = 0
height_effekt = 0

util.data_mapper { -- Empfaengt einen Wrt von main.py
    ["titel_sichtbar"] = function(value)
        titel_sichtbar = value
    end
}
util.data_mapper {
    ["effekt_fade"] = function(value)
        effekt_sichtbar = value
    end
}
util.data_mapper {
    ["effekt_zoom"] = function(value)
        effekt_sichtbar = 1
        width_effekt = value
        height_effekt = value
    end
}

--Rendere den Infobeamer   
function node.render()
    gl.clear(0, 0, 0, 1) -- schwarzer hintergrund

    -- Laden der Child-Objekte
    resource.render_child(hintergrund_child):draw(0, 0, WIDTH, HEIGHT, 1)
    resource.render_child(effekt_child):draw(WIDTH / 2 - width_effekt / 2, HEIGHT / 2 - height_effekt / 2, WIDTH / 2 + width_effekt / 2, HEIGHT / 2 + height_effekt / 2, effekt_sichtbar)
    resource.render_child(punkte_child):draw(256, 0, 768, 130, 1)

end
