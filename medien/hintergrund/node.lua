gl.setup(1024, 750)

local congress = resource.load_font("33c3.ttf")
local font = resource.load_font("Lato-Regular.ttf")
local video = resource.load_video{
    file = "matrix_animation.mp4";
    looped = true;
}
alpha = 1
titel = "Schwebedraht"
subtitel = "Ein Spiel der see-base"

util.data_mapper { --Daten via UDP Empfangen
    ["alpha"] = function(value) --an die Funktion punkte wird ein Wert uebergeben
        alpha = value  --Die Variable punkte im info-beamer hat den von Python3 uebergebenen Wert
    end
}

width_titel = font:width(titel, 120)
width_subtitel = font:width(subtitel, 60)

function node.render()
    gl.clear(1, 1, 0, 1)
    video:draw(0, 0, WIDTH, HEIGHT)
    font:write(WIDTH / 2 - width_titel / 2, 200, titel, 120, 1, 1, 0.4, alpha) -- Ueberschrift
    font:write(WIDTH / 2 - width_subtitel / 2, 380, subtitel, 60, 0.37, 0.73, 1, alpha) -- Ueberschrift
end
