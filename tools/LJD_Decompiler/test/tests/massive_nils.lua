-- The following turns into the following assignment when decompiled:
-- slot0, slot1 = nil
-- ... which then (with the bug unpatched) becomes a massive ref in slotworks, and breaks everything
local some_local, important_padding

-- Note that assigning anything else doesn't exhibit this problem. This is probably due to the KNIL instruction.
-- local some_local, important_padding = false, false

my_gbl   = some_local
my_gbl_2 = some_local

-- Make sure this works properly with table constructors
local a, b, c = nil
tbl = { a, b, c }

-- And that it keeps working when we use one of the variables more than once
-- This can break if the massive assignment gets invalidated but not all the slots
-- have been inlined
-- TODO the 'a' and 'c' variables get inlined and the compiler removes them since values are nil by default
local a, b, c = nil
tbl = { a, b, c }
print(b)

-- Check that massive nil expansion works properly with function calls
local z = nil
f(1, nil, nil, nil, z, 2)
