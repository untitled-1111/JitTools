-- Check how tolerant the expression unwarping is of dummy blocks in
-- the AST, caused by ISTC/ISFC instructions.

local value
value = gbl1 and gbl2 or gbl3

print(value)
