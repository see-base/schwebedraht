gl.setup(1024, 600)

local star = resource.load_image("star.png")
function node.render()
    --gl.clear(0, 1, 1, 1)
    star:draw(0, 0, WIDTH, HEIGHT)

end
