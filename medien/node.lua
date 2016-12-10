gl.setup(1024, 750)
node.set_flag "slow_gc"
node.gc()
--Hintergrund foo

local font = resource.load_font("Lato-Regular.ttf")

hintergrund_child = "hintergrund" -- Node fuer Hintergrund Bild/Animation/Wasauchimmer
effekt_child = "effekt" -- Node fuer Effekte bei einem Event
punkte_child = "punkte" -- Node fuer die Punkteanzeige

effekt_sichtbar = 0

zoom = 0
zoom_option = "plus"
z_option = 1 -- 0 for minus
zoom_multipler = 2
zoom_exponential = 0
zoom_expo = 0
z_fade = 2.3
zoom_fade = 1 --optionen fuer effektlaenge
zoom_fade_option = 0.05
starttime = 0

util.data_mapper {
    ["effekt_fade"] = function(value)
        effekt_sichtbar = value
    end
}
util.data_mapper {
    ["zoom"] = function(value)
        value= tonumber(value)
        zoom = value
        effekt_sichtbar = 1
        zoom_expo = 0 
        starttime = sys.now()
    end
}
util.data_mapper {
    ["zoom_multipler"] = function(value)
        zoom_multipler = value
        effekt_sichtbar = 0
    end
}
util.data_mapper {
    ["zoom_exponential"] = function(value)
        zoom_exponential = value
        effekt_sichtbar = 0
    end
}
util.data_mapper {
    ["zoom_option"] = function(value)
        zoom_option = value
        effekt_sichtbar = 0
        if zoom_option == "plus" then
             z_option = 1
        else
             z_option = 0
        end
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
    end
}
util.data_mapper {
    ["zoom_fade_option"] = function(value)
        zoom_fade_option = value + 0.1
        effekt_sichtbar = 0
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
    resource.render_child(effekt_child):draw(WIDTH / 2 - zoom / 2, HEIGHT / 2 - zoom / 2, WIDTH / 2 + zoom / 2, HEIGHT / 2 + zoom / 2, effekt_sichtbar):dispose()
    resource.render_child(punkte_child):draw(256, 0, 768, 130, 1):dispose()
end
