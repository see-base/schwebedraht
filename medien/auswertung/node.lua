gl.setup(1024, 750)
node.set_flag "slow_gc"
node.gc()

--Hintergrund foo
local congress = resource.load_font("33c3.ttf")
local font = resource.load_font("Lato-Regular.ttf")


--Rendere den Infobeamer   
function node.render()
    font:write(120, 320, "Hello World", 150, 1,1,1,1)



end
