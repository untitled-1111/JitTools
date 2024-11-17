-- Due to how the writer won't draw an object more than once, make sure that
-- this can't break the output.

local a, b, c = nil

tbl = { a, b, c }

local d, e, f = nil
for i in d,e,f do end

local h, i, j = nil
print(h, i, j)
