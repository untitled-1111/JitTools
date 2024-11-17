-- Check that passing upvalues through multiple functions works properly

local l1 = f()
local l2 = f()
local l3 = f()

function a()
    g1 = l1
    g2 = l2
    f = function()
        g2_b = l2
        g3 = l3
    end
end
