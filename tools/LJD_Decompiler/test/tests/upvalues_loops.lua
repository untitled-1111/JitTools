for i=1,10 do
	local j = 123
	gbl = function()
		return i, j
	end
end

for k, v in iter do
	local j = 123
	gbl = function()
		return k, j, v
	end
end
