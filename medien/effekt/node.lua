gl.setup(1024, 600)

bildname = "testbild.png"

local bild = resource.load_image(bildname)

util.data_mapper {
    ["bildname"] = function(value)
        bild:dispose()
        bild = resource.load_image(value)
    end
}

function node.render()
    --gl.clear(0, 1, 1, 1)
    bild:draw(0, 0, WIDTH, HEIGHT)

end
