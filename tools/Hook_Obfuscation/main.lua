local ffi = require('ffi')

local counterLoad = 1
local ioopen = io.open

local function start()
	ffi.cdef("int SetConsoleTitleA(const char* name)")
	ffi.C.SetConsoleTitleA("Lua hook load by The Spark blasthack")

	os.execute('cls')
end

start()

local getFilePathFromPathWithoutEx = function(path)
	return string.match(path, '(.+)%..+$')
end

local obfHook = function(code)
	local file_name = getFilePathFromPathWithoutEx(arg[1])
	local file = ioopen(file_name .. ' - [' .. counterLoad .. "].lua", "wb")

	counterLoad = counterLoad + 1
	if file then
		file:write(code)
		file:close()
	end
end

load_call = function(code)
	print(string.format(' \27[36mH | Load\27[0m [%d]', counterLoad))
	obfHook(code)
end

loadstring_call = function(code)
	print(string.format(' \27[36mH | Loadstring\27[0m [%d]', counterLoad))
	obfHook(code)
end


local fFunction, sErrorText = loadfile(arg[1])
if fFunction then
	local errorHandler = function(err)
		print(" \27[31mH | Error:\27[0m")
		print(err)
	end

	require('nop')
	xpcall(fFunction, errorHandler)
else
	print(' \27[31mH | Error in code:\27[0m')
	print(sErrorText)
end
