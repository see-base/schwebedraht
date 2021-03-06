gl.setup(1024, 750)
node.set_flag "slow_gc"
node.gc()
--Aenderungen von Funktionen bitte Dokumentieren!

--Hintergrund foo
local congress = resource.load_font("33c3.ttf")
local font = resource.load_font("Lato-Regular.ttf")

connected = "False" -- Ist der schwebedraht aktiv und sendet Daten zum Info-Beamer?

hintergrund_child = "hintergrund" -- Node fuer Hintergrund Bild/Animation/Wasauchimmer
effekt_child = "effekt" -- Node fuer Effekte bei einem Event
punkte_child = "punkte" -- Node fuer die Punkteanzeige
auswertung_child = "auswertung" -- Node fuer Auswertung / Spiel Ende
effekt_sichtbar = 0
auswertung = 0

zoom = 0
zoom_multipler = 2
zoom_exponential = 0
zoom_expo = 0
z_fade = 2.3
zoom_fade = 1 --optionen fuer effektlaenge
zoom_fade_option = 0.05
starttime = 0

util.data_mapper {
    ["ausw"] = function(value)
        auswertung = value
    end
}
util.data_mapper {
    ["effekt_fade"] = function(value)
        effekt_sichtbar = value
        connected = "True"
    end
}
util.data_mapper {
    ["zoom"] = function(value)
        value= tonumber(value)
        zoom = value
        effekt_sichtbar = 1
        zoom_expo = 0 
        connected = "True"
        starttime = sys.now()
    end
}
util.data_mapper {
    ["zoom_multipler"] = function(value)
        zoom_multipler = value
        effekt_sichtbar = 0
        connected = "True"
    end
}
util.data_mapper {
    ["zoom_exponential"] = function(value)
        zoom_exponential = value
        effekt_sichtbar = 0
        connected = "True"
    end
}
util.data_mapper {
    ["zoom_fade"] = function(value)
        zoom_fade = value
        effekt_sichtbar = 0
        if zoom_fade == "1" then
            z_fade = 2.3
        elseif zoom_fade == "2" then
            z_fade = 4.2
        else
            z_fade = 1
        end
        connected = "True"
    end
}
util.data_mapper {
    ["zoom_fade_option"] = function(value)
        zoom_fade_option = value + 0.1
        effekt_sichtbar = 0
        connected = "True"
    end
}
util.data_mapper {
    ["connected"] = function(value)
        connected = value
    end
}

--Rendere den Infobeamer   
function node.render()
    gl.clear(1, 0, 0, 1) -- roter hintergrund

   --Effekte:
    zoom = zoom + (sys.now() - starttime) * (zoom_multipler + zoom_expo)
    if ((sys.now() - starttime) > z_fade) then
        effekt_sichtbar=math.floor(100*(effekt_sichtbar - zoom_fade_option))/100
    end    
    zoom_expo = zoom_expo + zoom_exponential
    
    -- Laden der Child-Objekte
    hintergrund = resource.render_child(hintergrund_child):draw(0, 0, WIDTH, HEIGHT, 1):dispose()
    resource.render_child(auswertung_child):draw(0, 0, WIDTH, HEIGHT, auswertung):dispose()
    resource.render_child(effekt_child):draw(WIDTH / 2 - zoom / 2, HEIGHT / 2 - zoom / 2, WIDTH / 2 + zoom / 2, HEIGHT / 2 + zoom / 2, effekt_sichtbar):dispose()
    if (connected == "True") then
        resource.render_child(punkte_child):draw(256, 0, 768, 130, 1):dispose()
    end
end
