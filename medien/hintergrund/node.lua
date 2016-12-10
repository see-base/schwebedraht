gl.setup(1024, 750)

local font = resource.load_font("Lato-Regular.ttf")
local video = resource.load_video{
    file = "matrix_animation.mp4";
    looped = true;
}

titel = "Schwebedraht"
subtitel = "Ein Spiel der see-base"

width_titel = font:width(titel, 120)
width_subtitel = font:width(subtitel, 60)

function node.render()
    gl.clear(1, 1, 0, 1)
    video:draw(0, 0, WIDTH, HEIGHT)
    font:write(WIDTH / 2 - width_titel / 2, 200, titel, 120, 1, 1, 0.4, 1) -- Ueberschrift
    font:write(WIDTH / 2 - width_subtitel / 2, 380, subtitel, 60, 0.37, 0.73, 1, 1) -- Ueberschrift
end
