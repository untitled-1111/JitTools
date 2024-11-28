local ffi = require('ffi')


ffi.cdef("int SetConsoleTitleA(const char* name)")
ffi.C.SetConsoleTitleA("Lua hook load by The Spark blasthack")
os.execute('cls')

local getFilePathFromPathWithoutEx = function(path)
	return string.match(path, '(.+)%..+$')
end

local counterLoad = 1
local ioopen = io.open
local obfHook = function(code)
	local filePath = getFilePathFromPathWithoutEx(arg[1])
	local file = ioopen(filePath .. '-' .. counterLoad .. " - JitTools (H).lua", "wb")
	counterLoad = counterLoad + 1
	if file then
		file:write(code)
		file:close()
	end
end

load_call = function(code)
	print('Detect load! ' .. counterLoad)
	obfHook(code)
end

loadstring_call = function(code)
	print('Detect loadstring! ' .. counterLoad)
	obfHook(code)
end


local fFunction, sErrorText = loadfile(arg[1])
if fFunction then
	local errorHandler = function(err)
		print("Error:")
		print(err)
	end

	require('nop')
	xpcall(fFunction, errorHandler)
else
	print('Error load script:')
	print(sErrorText)
end
