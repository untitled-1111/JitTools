-- Check that the iterator slot is correctly handled if it's been used previously

local a,b,c,d,e,f = 1,2,3,4,5,6

for i=1,10 do
	print(i)
end

for i, j, k in zz() do
	print(i, j, k)
end
