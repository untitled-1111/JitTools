-- Make sure upvalues work when the upvalue was defined
-- in a different block to the function.

local l = 123

-- Test defining a function inside a block
if gbl then
	gbl = function()
		return l
	end
end

-- And outside the block
gbl = function()
	return l
end
