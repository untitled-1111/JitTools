-- Make sure that the assignment to mytbl.abc doesn't get pulled into
-- the table constructor, since it's in a different block.
local mytbl = {}

if gbl_1 then
	mytbl.abc = 123
end

gbl_2 = mytbl
