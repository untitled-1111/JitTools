-- Check that function calls and table reads/writes can't be reordered in a manner that
-- changes the order in which they are executed.

-- Relatively plausable code
-- If measures aren't taken to prevent this, get() might be inlined and run after set()
local v = get()
set()
print(v)

-- Same goes for reads, as the function environment might have a metatable with an __index function
local vv = gbl
set_gbl()
print(vv)

-- Even something as simple as this will have slightly different behaviour after slot
-- elimination, since the global gets and addition will be reordered.
local l = g + 1
print(l)

-- Check that a mixture of pulled out and normal arguments are handled correctly
local l = f()
print(f1(), gbl1, l, f2(), gbl2)
