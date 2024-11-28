-- Make sure the decompiler properly handles method syntax for function declarations and calls

function Obj:f()
	print(self)
end

gbl.f()

gbl:f()

local a = gbl
print(a)
a:f()
