-- Make sure the loop verification code doesn't get caught on blocks
-- flowing to a later block when a loop is involved.

-- We need it as a local, use it more than once to block inlining, since
-- that'll fail the test.
local z = gbl
print(z)

f(z and x)

while gbl_2 do
	f()
end
