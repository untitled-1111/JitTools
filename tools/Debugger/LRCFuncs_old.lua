-- fix it pls

local jit = require 'jit.bc'
local dumper = require("LRCDumper")(jit)

local l  = {}

l.wait = function(...)
    print('called wait(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    return true
end

l.isSampAvailable = function(...)
    print('called isSampAvailable(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    return true
end

l.coroutine = {}
l.coroutine["wrap"] = function(...)
    print('called coroutine.wrap(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['wrap'](...)
    print("\x1b[33mresult of call", "coroutine.wrap", res, "\x1b[36m")
    return res
end
l.coroutine["yield"] = function(...)
    print('called coroutine.yield(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['yield'](...)
    print("\x1b[33mresult of call", "coroutine.yield", res, "\x1b[36m")
    return res
end
l.coroutine["resume"] = function(...)
    print('called coroutine.resume(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['resume'](...)
    print("\x1b[33mresult of call", "coroutine.resume", res, "\x1b[36m")
    return res
end
l.coroutine["status"] = function(...)
    print('called coroutine.status(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['status'](...)
    print("\x1b[33mresult of call", "coroutine.status", res, "\x1b[36m")
    return res
end
l.coroutine["isyieldable"] = function(...)
    print('called coroutine.isyieldable(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['isyieldable'](...)
    print("\x1b[33mresult of call", "coroutine.isyieldable", res, "\x1b[36m")
    return res
end
l.coroutine["running"] = function(...)
    print('called coroutine.running(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['running'](...)
    print("\x1b[33mresult of call", "coroutine.running", res, "\x1b[36m")
    return res
end
l.coroutine["create"] = function(...)
    print('called coroutine.create(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = coroutine['create'](...)
    print("\x1b[33mresult of call", "coroutine.create", res, "\x1b[36m")
    return res
end
l.assert = function(...)
    print('called assert(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = assert(...)
    print("\x1b[33mresult of call", "assert", res, "\x1b[36m")
    return res
end
l.tostring = function(...)
    print('called tostring(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = tostring(...)
    print("\x1b[33mresult of call", "tostring", res, "\x1b[36m")
    return res
end
l.tonumber = function(...)
    --print('called tonumber(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = tonumber(...)
    --print("\x1b[33mresult of call", "tonumber", res, "\x1b[36m")
    return res
end
l.io = {}
l.io["input"] = function(...)
    print('called io.input(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['input'](...)
    print("\x1b[33mresult of call", "io.input", res, "\x1b[36m")
    return res
end
l.io["tmpfile"] = function(...)
    print('called io.tmpfile(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['tmpfile'](...)
    print("\x1b[33mresult of call", "io.tmpfile", res, "\x1b[36m")
    return res
end
l.io["read"] = function(...)
    print('called io.read(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['read'](...)
    print("\x1b[33mresult of call", "io.read", res, "\x1b[36m")
    return res
end
l.io["output"] = function(...)
    print('called io.output(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['output'](...)
    print("\x1b[33mresult of call", "io.output", res, "\x1b[36m")
    return res
end
l.io["open"] = function(...)
    --print('called io.open(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['open'](...)
	print("\x1b[33mresult of call", "io.open", res, "\x1b[36m")
    return res
end
l.io["close"] = function(...)
    print('called io.close(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['close'](...)
    print("\x1b[33mresult of call", "io.close", res, "\x1b[36m")
    return res
end
l.io["write"] = function(...)
    print('called io.write(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['write'](...)
    print("\x1b[33mresult of call", "io.write", res, "\x1b[36m")
    return res
end
l.io["popen"] = function(...)
    print('called io.popen(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['popen'](...)
    print("\x1b[33mresult of call", "io.popen", res, "\x1b[36m")
    return res
end
l.io["flush"] = function(...)
    print('called io.flush(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['flush'](...)
    print("\x1b[33mresult of call", "io.flush", res, "\x1b[36m")
    return res
end
l.io["type"] = function(...)
    print('called io.type(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['type'](...)
    print("\x1b[33mresult of call", "io.type", res, "\x1b[36m")
    return res
end
l.io["lines"] = function(...)
    print('called io.lines(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = io['lines'](...)
    print("\x1b[33mresult of call", "io.lines", res, "\x1b[36m")
    return res
end
l.rawget = function(...)
    print('called rawget(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = rawget(...)
    print("\x1b[33mresult of call", "rawget", res, "\x1b[36m")
    return res
end
l.xpcall = function(...)
    print('called xpcall(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = xpcall(...)
    print("\x1b[33mresult of call", "xpcall", res, "\x1b[36m")
    return res
end
l.arg = {}
l.ipairs = function(...)
    print('called ipairs(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = ipairs(...)
    print("\x1b[33mresult of call", "ipairs", res, "\x1b[36m")
    return res
end
l.print = function(...)
    print('called print(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = print(...)
    print("\x1b[33mresult of call", "print", res, "\x1b[36m")
    return res
end
l.pcall = function(func, ...)
    print('called pcall(\x1b[35m', func ,'\x1b[36m)')
    local res = pcall(func, ...)
    print("\x1b[33mresult of call", "pcall", res, "\x1b[36m")
    return res
end
l.gcinfo = function(...)
    print('called gcinfo(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = gcinfo(...)
    print("\x1b[33mresult of call", "gcinfo", res, "\x1b[36m")
    return res
end
l.module = function(...)
    print('called module(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = module(...)
    print("\x1b[33mresult of call", "module", res, "\x1b[36m")
    return res
end
l.setfenv = function(...)
    print('called setfenv(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = setfenv(...)
    print("\x1b[33mresult of call", "setfenv", res, "\x1b[36m")
    return res
end
l.jit = {}
l.jit["status"] = function(...)
    print('called jit.status(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit['status'](...)
    print("\x1b[33mresult of call", "jit.status", res, "\x1b[36m")
    return res
end
l.jit["on"] = function(...)
    print('called jit.on(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit['on'](...)
    print("\x1b[33mresult of call", "jit.on", res, "\x1b[36m")
    return res
end
l.jit["off"] = function(...)
    print('called jit.off(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit['off'](...)
    print("\x1b[33mresult of call", "jit.off", res, "\x1b[36m")
    return res
end
l.jit["flush"] = function(...)
    print('called jit.flush(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit['flush'](...)
    print("\x1b[33mresult of call", "jit.flush", res, "\x1b[36m")
    return res
end
l.jit["attach"] = function(...)
    print('called jit.attach(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit['attach'](...)
    print("\x1b[33mresult of call", "jit.attach", res, "\x1b[36m")
    return res
end
l.jit.opt = {}
l.jit.opt["start"] = function(...)
    print('called jit.opt.start(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = jit.opt['start'](...)
    print("\x1b[33mresult of call", "jit.opt.start", res, "\x1b[36m")
    return res
end
l.pairs = function(...)
    --print('called pairs(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = pairs(...)
    --print("\x1b[33mresult of call", "pairs", res, "\x1b[36m")
    return res
end
l.bit = {}
l.bit["rol"] = function(...)
    print('called bit.rol(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['rol'](...)
    print("\x1b[33mresult of call", "bit.rol", res, "\x1b[36m")
    return res
end
l.bit["rshift"] = function(...)
    print('called bit.rshift(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['rshift'](...)
    print("\x1b[33mresult of call", "bit.rshift", res, "\x1b[36m")
    return res
end
l.bit["ror"] = function(...)
    print('called bit.ror(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['ror'](...)
    print("\x1b[33mresult of call", "bit.ror", res, "\x1b[36m")
    return res
end
l.bit["bswap"] = function(...)
    print('called bit.bswap(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['bswap'](...)
    print("\x1b[33mresult of call", "bit.bswap", res, "\x1b[36m")
    return res
end
l.bit["bxor"] = function(...)
    print('called bit.bxor(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['bxor'](...)
    print("\x1b[33mresult of call", "bit.bxor", res, "\x1b[36m")
    return res
end
l.bit["bor"] = function(...)
    print('called bit.bor(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['bor'](...)
    print("\x1b[33mresult of call", "bit.bor", res, "\x1b[36m")
    return res
end
l.bit["arshift"] = function(...)
    print('called bit.arshift(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['arshift'](...)
    print("\x1b[33mresult of call", "bit.arshift", res, "\x1b[36m")
    return res
end
l.bit["bnot"] = function(...)
    print('called bit.bnot(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['bnot'](...)
    print("\x1b[33mresult of call", "bit.bnot", res, "\x1b[36m")
    return res
end
l.bit["tobit"] = function(...)
    print('called bit.tobit(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['tobit'](...)
    print("\x1b[33mresult of call", "bit.tobit", res, "\x1b[36m")
    return res
end
l.bit["lshift"] = function(...)
    print('called bit.lshift(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['lshift'](...)
    print("\x1b[33mresult of call", "bit.lshift", res, "\x1b[36m")
    return res
end
l.bit["tohex"] = function(...)
    print('called bit.tohex(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['tohex'](...)
    print("\x1b[33mresult of call", "bit.tohex", res, "\x1b[36m")
    return res
end
l.bit["band"] = function(...)
    print('called bit.band(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = bit['band'](...)
    print("\x1b[33mresult of call", "bit.band", res, "\x1b[36m")
    return res
end
l.debug = {}
l.debug["setupvalue"] = function(...)
    print('called debug.setupvalue(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['setupvalue'](...)
    print("\x1b[33mresult of call", "debug.setupvalue", res, "\x1b[36m")
    return res
end
l.debug["getregistry"] = function(...)
    print('called debug.getregistry(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getregistry'](...)
    print("\x1b[33mresult of call", "debug.getregistry", res, "\x1b[36m")
    return res
end
l.debug["traceback"] = function(...)
    print('called debug.traceback(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['traceback'](...)
    print("\x1b[33mresult of call", "debug.traceback", res, "\x1b[36m")
    return res
end
l.debug["setlocal"] = function(...)
    print('called debug.setlocal(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['setlocal'](...)
    print("\x1b[33mresult of call", "debug.setlocal", res, "\x1b[36m")
    return res
end
l.debug["getupvalue"] = function(...)
    print('called debug.getupvalue(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getupvalue'](...)
    print("\x1b[33mresult of call", "debug.getupvalue", res, "\x1b[36m")
    return res
end
l.debug["gethook"] = function(...)
    print('called debug.gethook(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['gethook'](...)
    print("\x1b[33mresult of call", "debug.gethook", res, "\x1b[36m")
    return res
end
l.debug["sethook"] = function(...)
    print('called debug.sethook(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['sethook'](...)
    print("\x1b[33mresult of call", "debug.sethook", res, "\x1b[36m")
    return res
end
l.debug["getlocal"] = function(...)
    print('called debug.getlocal(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getlocal'](...)
    print("\x1b[33mresult of call", "debug.getlocal", res, "\x1b[36m")
    return res
end
l.debug["upvaluejoin"] = function(...)
    print('called debug.upvaluejoin(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['upvaluejoin'](...)
    print("\x1b[33mresult of call", "debug.upvaluejoin", res, "\x1b[36m")
    return res
end
l.debug["getinfo"] = function(...)
    print('called debug.getinfo(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getinfo'](...)
    print("\x1b[33mresult of call", "debug.getinfo", res, "\x1b[36m")
    return res
end
l.debug["getfenv"] = function(...)
    print('called debug.getfenv(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getfenv'](...)
    print("\x1b[33mresult of call", "debug.getfenv", res, "\x1b[36m")
    return res
end
l.debug["setmetatable"] = function(...)
    print('called debug.setmetatable(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['setmetatable'](...)
    print("\x1b[33mresult of call", "debug.setmetatable", res, "\x1b[36m")
    return res
end
l.debug["upvalueid"] = function(...)
    print('called debug.upvalueid(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['upvalueid'](...)
    print("\x1b[33mresult of call", "debug.upvalueid", res, "\x1b[36m")
    return res
end
l.debug["getuservalue"] = function(...)
    print('called debug.getuservalue(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getuservalue'](...)
    print("\x1b[33mresult of call", "debug.getuservalue", res, "\x1b[36m")
    return res
end
l.debug["debug"] = function(...)
    print('called debug.debug(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['debug'](...)
    print("\x1b[33mresult of call", "debug.debug", res, "\x1b[36m")
    return res
end
l.debug["getmetatable"] = function(...)
    print('called debug.getmetatable(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['getmetatable'](...)
    print("\x1b[33mresult of call", "debug.getmetatable", res, "\x1b[36m")
    return res
end
l.debug["setfenv"] = function(...)
    print('called debug.setfenv(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['setfenv'](...)
    print("\x1b[33mresult of call", "debug.setfenv", res, "\x1b[36m")
    return res
end
l.debug["setuservalue"] = function(...)
    print('called debug.setuservalue(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = debug['setuservalue'](...)
    print("\x1b[33mresult of call", "debug.setuservalue", res, "\x1b[36m")
    return res
end
l.package = {}
l.package.preload = {}
l.package.preload["table.clear"] = function(...)
    print('called package.preload.table.clear(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.preload['table.clear'](...)
    print("\x1b[33mresult of call", "package.preload.table.clear", res, "\x1b[36m")
    return res
end
l.package.preload["ffi"] = function(...)
    print('called package.preload.ffi(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.preload['ffi'](...)
    print("\x1b[33mresult of call", "package.preload.ffi", res, "\x1b[36m")
    return res
end
l.package.preload["jit.util"] = function(...)
    print('called package.preload.jit.util(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.preload['jit.util'](...)
    print("\x1b[33mresult of call", "package.preload.jit.util", res, "\x1b[36m")
    return res
end
l.package.preload["table.new"] = function(...)
    print('called package.preload.table.new(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.preload['table.new'](...)
    print("\x1b[33mresult of call", "package.preload.table.new", res, "\x1b[36m")
    return res
end
l.package.preload["jit.profile"] = function(...)
    print('called package.preload.jit.profile(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.preload['jit.profile'](...)
    print("\x1b[33mresult of call", "package.preload.jit.profile", res, "\x1b[36m")
    return res
end
l.package.loaded = {}
l.package.loaded.coroutine = {}
l.package.loaded.coroutine["wrap"] = function(...)
    print('called package.loaded.coroutine.wrap(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['wrap'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.wrap", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["yield"] = function(...)
    print('called package.loaded.coroutine.yield(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['yield'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.yield", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["resume"] = function(...)
    print('called package.loaded.coroutine.resume(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['resume'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.resume", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["status"] = function(...)
    print('called package.loaded.coroutine.status(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['status'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.status", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["isyieldable"] = function(...)
    print('called package.loaded.coroutine.isyieldable(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['isyieldable'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.isyieldable", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["running"] = function(...)
    print('called package.loaded.coroutine.running(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['running'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.running", res, "\x1b[36m")
    return res
end
l.package.loaded.coroutine["create"] = function(...)
    print('called package.loaded.coroutine.create(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.coroutine['create'](...)
    print("\x1b[33mresult of call", "package.loaded.coroutine.create", res, "\x1b[36m")
    return res
end
l.package.loaded.jit = {}
l.package.loaded.jit.opt = {}
l.package.loaded.jit.opt["start"] = function(...)
    print('called package.loaded.jit.opt.start(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.jit.opt['start'](...)
    print("\x1b[33mresult of call", "package.loaded.jit.opt.start", res, "\x1b[36m")
    return res
end
l.package.loaded.math = {}
l.package.loaded.math["ceil"] = function(...)
    print('called package.loaded.math.ceil(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['ceil'](...)
    print("\x1b[33mresult of call", "package.loaded.math.ceil", res, "\x1b[36m")
    return res
end
l.package.loaded.math["tan"] = function(...)
    print('called package.loaded.math.tan(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['tan'](...)
    print("\x1b[33mresult of call", "package.loaded.math.tan", res, "\x1b[36m")
    return res
end
l.package.loaded.math["log10"] = function(...)
    print('called package.loaded.math.log10(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['log10'](...)
    print("\x1b[33mresult of call", "package.loaded.math.log10", res, "\x1b[36m")
    return res
end
l.package.loaded.math["randomseed"] = function(...)
    print('called package.loaded.math.randomseed(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['randomseed'](...)
    print("\x1b[33mresult of call", "package.loaded.math.randomseed", res, "\x1b[36m")
    return res
end
l.package.loaded.math["cos"] = function(...)
    print('called package.loaded.math.cos(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['cos'](...)
    print("\x1b[33mresult of call", "package.loaded.math.cos", res, "\x1b[36m")
    return res
end
l.package.loaded.math["sinh"] = function(...)
    print('called package.loaded.math.sinh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['sinh'](...)
    print("\x1b[33mresult of call", "package.loaded.math.sinh", res, "\x1b[36m")
    return res
end
l.package.loaded.math["random"] = function(...)
    print('called package.loaded.math.random(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['random'](...)
    print("\x1b[33mresult of call", "package.loaded.math.random", res, "\x1b[36m")
    return res
end
l.package.loaded.math["max"] = function(...)
    print('called package.loaded.math.max(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['max'](...)
    print("\x1b[33mresult of call", "package.loaded.math.max", res, "\x1b[36m")
    return res
end
l.package.loaded.math["atan2"] = function(...)
    print('called package.loaded.math.atan2(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['atan2'](...)
    print("\x1b[33mresult of call", "package.loaded.math.atan2", res, "\x1b[36m")
    return res
end
l.package.loaded.math["ldexp"] = function(...)
    print('called package.loaded.math.ldexp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['ldexp'](...)
    print("\x1b[33mresult of call", "package.loaded.math.ldexp", res, "\x1b[36m")
    return res
end
l.package.loaded.math["floor"] = function(...)
    print('called package.loaded.math.floor(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['floor'](...)
    print("\x1b[33mresult of call", "package.loaded.math.floor", res, "\x1b[36m")
    return res
end
l.package.loaded.math["sqrt"] = function(...)
    print('called package.loaded.math.sqrt(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['sqrt'](...)
    print("\x1b[33mresult of call", "package.loaded.math.sqrt", res, "\x1b[36m")
    return res
end
l.package.loaded.math["deg"] = function(...)
    print('called package.loaded.math.deg(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['deg'](...)
    print("\x1b[33mresult of call", "package.loaded.math.deg", res, "\x1b[36m")
    return res
end
l.package.loaded.math["atan"] = function(...)
    print('called package.loaded.math.atan(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['atan'](...)
    print("\x1b[33mresult of call", "package.loaded.math.atan", res, "\x1b[36m")
    return res
end
l.package.loaded.math["fmod"] = function(...)
    print('called package.loaded.math.fmod(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['fmod'](...)
    print("\x1b[33mresult of call", "package.loaded.math.fmod", res, "\x1b[36m")
    return res
end
l.package.loaded.math["acos"] = function(...)
    print('called package.loaded.math.acos(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['acos'](...)
    print("\x1b[33mresult of call", "package.loaded.math.acos", res, "\x1b[36m")
    return res
end
l.package.loaded.math["pow"] = function(...)
    print('called package.loaded.math.pow(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['pow'](...)
    print("\x1b[33mresult of call", "package.loaded.math.pow", res, "\x1b[36m")
    return res
end
l.package.loaded.math["abs"] = function(...)
    print('called package.loaded.math.abs(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['abs'](...)
    print("\x1b[33mresult of call", "package.loaded.math.abs", res, "\x1b[36m")
    return res
end
l.package.loaded.math["min"] = function(...)
    print('called package.loaded.math.min(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['min'](...)
    print("\x1b[33mresult of call", "package.loaded.math.min", res, "\x1b[36m")
    return res
end
l.package.loaded.math["sin"] = function(...)
    print('called package.loaded.math.sin(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['sin'](...)
    print("\x1b[33mresult of call", "package.loaded.math.sin", res, "\x1b[36m")
    return res
end
l.package.loaded.math["frexp"] = function(...)
    print('called package.loaded.math.frexp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['frexp'](...)
    print("\x1b[33mresult of call", "package.loaded.math.frexp", res, "\x1b[36m")
    return res
end
l.package.loaded.math["log"] = function(...)
    print('called package.loaded.math.log(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['log'](...)
    print("\x1b[33mresult of call", "package.loaded.math.log", res, "\x1b[36m")
    return res
end
l.package.loaded.math["tanh"] = function(...)
    print('called package.loaded.math.tanh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['tanh'](...)
    print("\x1b[33mresult of call", "package.loaded.math.tanh", res, "\x1b[36m")
    return res
end
l.package.loaded.math["exp"] = function(...)
    print('called package.loaded.math.exp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['exp'](...)
    print("\x1b[33mresult of call", "package.loaded.math.exp", res, "\x1b[36m")
    return res
end
l.package.loaded.math["modf"] = function(...)
    print('called package.loaded.math.modf(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['modf'](...)
    print("\x1b[33mresult of call", "package.loaded.math.modf", res, "\x1b[36m")
    return res
end
l.package.loaded.math["cosh"] = function(...)
    print('called package.loaded.math.cosh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['cosh'](...)
    print("\x1b[33mresult of call", "package.loaded.math.cosh", res, "\x1b[36m")
    return res
end
l.package.loaded.math["asin"] = function(...)
    print('called package.loaded.math.asin(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['asin'](...)
    print("\x1b[33mresult of call", "package.loaded.math.asin", res, "\x1b[36m")
    return res
end
l.package.loaded.math["rad"] = function(...)
    print('called package.loaded.math.rad(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaded.math['rad'](...)
    print("\x1b[33mresult of call", "package.loaded.math.rad", res, "\x1b[36m")
    return res
end
l.package["seeall"] = function(...)
    print('called package.seeall(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package['seeall'](...)
    print("\x1b[33mresult of call", "package.seeall", res, "\x1b[36m")
    return res
end
l.package["loadlib"] = function(...)
    print('called package.loadlib(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package['loadlib'](...)
    print("\x1b[33mresult of call", "package.loadlib", res, "\x1b[36m")
    return res
end
l.package.searchers = {}
l.package.searchers["1"] = function(...)
    print('called package.searchers.1(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.searchers['1'](...)
    print("\x1b[33mresult of call", "package.searchers.1", res, "\x1b[36m")
    return res
end
l.package.searchers["2"] = function(...)
    print('called package.searchers.2(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.searchers['2'](...)
    print("\x1b[33mresult of call", "package.searchers.2", res, "\x1b[36m")
    return res
end
l.package.searchers["3"] = function(...)
    print('called package.searchers.3(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.searchers['3'](...)
    print("\x1b[33mresult of call", "package.searchers.3", res, "\x1b[36m")
    return res
end
l.package.searchers["4"] = function(...)
    print('called package.searchers.4(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.searchers['4'](...)
    print("\x1b[33mresult of call", "package.searchers.4", res, "\x1b[36m")
    return res
end
l.package["searchpath"] = function(...)
    print('called package.searchpath(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package['searchpath'](...)
    print("\x1b[33mresult of call", "package.searchpath", res, "\x1b[36m")
    return res
end
l.package.loaders = {}
l.package.loaders["1"] = function(...)
    print('called package.loaders.1(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaders['1'](...)
    print("\x1b[33mresult of call", "package.loaders.1", res, "\x1b[36m")
    return res
end
l.package.loaders["2"] = function(...)
    print('called package.loaders.2(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaders['2'](...)
    print("\x1b[33mresult of call", "package.loaders.2", res, "\x1b[36m")
    return res
end
l.package.loaders["3"] = function(...)
    print('called package.loaders.3(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaders['3'](...)
    print("\x1b[33mresult of call", "package.loaders.3", res, "\x1b[36m")
    return res
end
l.package.loaders["4"] = function(...)
    print('called package.loaders.4(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = package.loaders['4'](...)
    print("\x1b[33mresult of call", "package.loaders.4", res, "\x1b[36m")
    return res
end
l.error = function(...)
    print('called error(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = error(...)
    print("\x1b[33mresult of call", "error", res, "\x1b[36m")
    return res
end
l.load = function(code)
    print('called load(\x1b[35m'..code..'\x1b[36m)')
    local f = io.open("dumps\\" .. getFileNameFromPathWithoutEx(arg[1]) .. "_load_call.txt", "wb")
    f:write(code)
    f:close()
    local res = load(code)
    print("\x1b[33mresult of call", "load", res, "\x1b[36m")
    if res then
        if type(res) == "function" then
            print("\x1b[33mCalling res of", "load", res, "\x1b[36m")
            res()
        end
    end
    return res
end
l.loadfile = function(...)
    print('called loadfile(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = loadfile(...)
    print("\x1b[33mresult of call", "loadfile", res, "\x1b[36m")
    return res
end
l.rawequal = function(...)
    print('called rawequal(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = rawequal(...)
    print("\x1b[33mresult of call", "rawequal", res, "\x1b[36m")
    return res
end
l.string = {}
l.string["find"] = function(a, b, c, d)
    --print('called string.find(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['find'](a, b, c, d)
    --print("\x1b[33mresult of call", "string.find", res, "\x1b[36m")
    return res
end
l.string["format"] = function(...)
    print('called string.format(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['format'](...)
    print("\x1b[33mresult of call", "string.format", res, "\x1b[36m")
    return res
end
l.string["rep"] = function(...)
    print('called string.rep(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['rep'](...)
    print("\x1b[33mresult of call", "string.rep", res, "\x1b[36m")
    return res
end
l.string["gsub"] = function(...)
    print('called string.gsub(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['gsub'](...)
    print("\x1b[33mresult of call", "string.gsub", res, "\x1b[36m")
    return res
end
l.string["len"] = function(...)
    --print('called string.len(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['len'](...)
    --print("\x1b[33mresult of call", "string.len", res, "\x1b[36m")
    return res
end
l.string["gmatch"] = function(code, pattern)
    print('called string.gmatch(\x1b[35m'..code..'\x1b[36m)')
    local res = string['gmatch'](code, pattern)
    print("\x1b[33mresult of call", "string.gmatch", res, "\x1b[36m")
    return res
end
l.string["dump"] = function(...)
    print('called string.dump(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['dump'](...)
    print("\x1b[33mresult of call", "string.dump", res, "\x1b[36m")
    return res
end
l.string["match"] = function(...)
    print('called string.match(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['match'](...)
    print("\x1b[33mresult of call", "string.match", res, "\x1b[36m")
    return res
end
l.string["reverse"] = function(...)
   -- print('called string.reverse(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['reverse'](...)
    --print("\x1b[33mresult of call", "string.reverse", res, "\x1b[36m")
    return res
end
l.string["byte"] = function(...)
    --print('called string.byte(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['byte'](...)
   -- print("\x1b[33mresult of call", "string.byte", res, "\x1b[36m")
    return res
end
l.string["char"] = function(...)
    --print('called string.char(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['char'](...)
    --print("\x1b[33mresult of call", "string.char", res, "\x1b[36m")
    return res
end
l.string["upper"] = function(...)
    print('called string.upper(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['upper'](...)
    print("\x1b[33mresult of call", "string.upper", res, "\x1b[36m")
    return res
end
l.string["lower"] = function(...)
    print('called string.lower(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['lower'](...)
    print("\x1b[33mresult of call", "string.lower", res, "\x1b[36m")
    return res
end
l.string["sub"] = function(...)
    print('called string.sub(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = string['sub'](...)
    print("\x1b[33mresult of call", "string.sub", res, "\x1b[36m")
    return res
end
l.unpack = function(...)
    print('called unpack(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = unpack(...)
    print("\x1b[33mresult of call", "unpack", res, "\x1b[36m")
    return res
end
l.table = {}
l.table["maxn"] = function(...)
    print('called table.maxn(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['maxn'](...)
    print("\x1b[33mresult of call", "table.maxn", res, "\x1b[36m")
    return res
end
l.table["move"] = function(...)
    print('called table.move(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['move'](...)
    print("\x1b[33mresult of call", "table.move", res, "\x1b[36m")
    return res
end
l.table["pack"] = function(...)
    print('called table.pack(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['pack'](...)
    print("\x1b[33mresult of call", "table.pack", res, "\x1b[36m")
    return res
end
l.table["foreach"] = function(...)
    print('called table.foreach(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['foreach'](...)
    print("\x1b[33mresult of call", "table.foreach", res, "\x1b[36m")
    return res
end
l.table["sort"] = function(...)
    print('called table.sort(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['sort'](...)
    print("\x1b[33mresult of call", "table.sort", res, "\x1b[36m")
    return res
end
l.table["remove"] = function(...)
    print('called table.remove(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['remove'](...)
    print("\x1b[33mresult of call", "table.remove", res, "\x1b[36m")
    return res
end
l.table["foreachi"] = function(...)
    print('called table.foreachi(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['foreachi'](...)
    print("\x1b[33mresult of call", "table.foreachi", res, "\x1b[36m")
    return res
end
l.table["unpack"] = function(...)
    print('called table.unpack(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['unpack'](...)
    print("\x1b[33mresult of call", "table.unpack", res, "\x1b[36m")
    return res
end
l.table["getn"] = function(...)
    print('called table.getn(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['getn'](...)
    print("\x1b[33mresult of call", "table.getn", res, "\x1b[36m")
    return res
end
l.table["concat"] = function(...)
    --print('called table.concat(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['concat'](...)
    --print("\x1b[33mresult of call", "table.concat", res, "\x1b[36m")
    return res
end
l.table["insert"] = function(...)
    print('called table.insert(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = table['insert'](...)
    print("\x1b[33mresult of call", "table.insert", res, "\x1b[36m")
    return res
end
l.require = function(lib)
    print('called require(\x1b[35m'..lib..'\x1b[36m)')
    if lib == "ffi" then
        return {cdef = function() end, new = function() end, C = {GetVolumeInformationA = function() return 1 end}, load = function() end}
    end
    --local res = require(...)
    --print("\x1b[33mresult of call", "require", res, "\x1b[36m")
    return {}
end
l.newproxy = function(...)
    print('called newproxy(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = newproxy(...)
    print("\x1b[33mresult of call", "newproxy", res, "\x1b[36m")
    return res
end
l.dofile = function(...)
    print('called dofile(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = dofile(...)
    print("\x1b[33mresult of call", "dofile", res, "\x1b[36m")
    return res
end
l.collectgarbage = function(...)
    print('called collectgarbage(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = collectgarbage(...)
    print("\x1b[33mresult of call", "collectgarbage", res, "\x1b[36m")
    return res
end
l.loadstring = function(...)
    print('called loadstring(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = loadstring(...)
    print("\x1b[33mresult of call", "loadstring", res, "\x1b[36m")
    return res
end
l.next = function(...)
    print('called next(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = next(...)
    print("\x1b[33mresult of call", "next", res, "\x1b[36m")
    return res
end
l.math = {}
l.math["ceil"] = function(...)
    print('called math.ceil(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['ceil'](...)
    print("\x1b[33mresult of call", "math.ceil", res, "\x1b[36m")
    return res
end
l.math["tan"] = function(...)
    print('called math.tan(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['tan'](...)
    print("\x1b[33mresult of call", "math.tan", res, "\x1b[36m")
    return res
end
l.math["log10"] = function(...)
    print('called math.log10(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['log10'](...)
    print("\x1b[33mresult of call", "math.log10", res, "\x1b[36m")
    return res
end
l.math["randomseed"] = function(...)
    print('called math.randomseed(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['randomseed'](...)
    print("\x1b[33mresult of call", "math.randomseed", res, "\x1b[36m")
    return res
end
l.math["cos"] = function(...)
    print('called math.cos(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['cos'](...)
    print("\x1b[33mresult of call", "math.cos", res, "\x1b[36m")
    return res
end
l.math["sinh"] = function(...)
    print('called math.sinh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['sinh'](...)
    print("\x1b[33mresult of call", "math.sinh", res, "\x1b[36m")
    return res
end
l.math["random"] = function(...)
    --print('called math.random(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['random'](...)
    --print("\x1b[33mresult of call", "math.random", res, "\x1b[36m")
    return res
end
l.math["max"] = function(...)
    print('called math.max(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['max'](...)
    print("\x1b[33mresult of call", "math.max", res, "\x1b[36m")
    return res
end
l.math["atan2"] = function(...)
    print('called math.atan2(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['atan2'](...)
    print("\x1b[33mresult of call", "math.atan2", res, "\x1b[36m")
    return res
end
l.math["ldexp"] = function(...)
    print('called math.ldexp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['ldexp'](...)
    print("\x1b[33mresult of call", "math.ldexp", res, "\x1b[36m")
    return res
end
l.math["floor"] = function(...)
    print('called math.floor(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['floor'](...)
    print("\x1b[33mresult of call", "math.floor", res, "\x1b[36m")
    return res
end
l.math["sqrt"] = function(...)
    print('called math.sqrt(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['sqrt'](...)
    print("\x1b[33mresult of call", "math.sqrt", res, "\x1b[36m")
    return res
end
l.math["deg"] = function(...)
    print('called math.deg(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['deg'](...)
    print("\x1b[33mresult of call", "math.deg", res, "\x1b[36m")
    return res
end
l.math["atan"] = function(...)
    print('called math.atan(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['atan'](...)
    print("\x1b[33mresult of call", "math.atan", res, "\x1b[36m")
    return res
end
l.math["fmod"] = function(...)
    print('called math.fmod(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['fmod'](...)
    print("\x1b[33mresult of call", "math.fmod", res, "\x1b[36m")
    return res
end
l.math["acos"] = function(...)
    print('called math.acos(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['acos'](...)
    print("\x1b[33mresult of call", "math.acos", res, "\x1b[36m")
    return res
end
l.math["pow"] = function(...)
    print('called math.pow(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['pow'](...)
    print("\x1b[33mresult of call", "math.pow", res, "\x1b[36m")
    return res
end
l.math["abs"] = function(...)
    print('called math.abs(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['abs'](...)
    print("\x1b[33mresult of call", "math.abs", res, "\x1b[36m")
    return res
end
l.math["min"] = function(...)
    print('called math.min(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['min'](...)
    print("\x1b[33mresult of call", "math.min", res, "\x1b[36m")
    return res
end
l.math["sin"] = function(...)
    print('called math.sin(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['sin'](...)
    print("\x1b[33mresult of call", "math.sin", res, "\x1b[36m")
    return res
end
l.math["frexp"] = function(...)
    print('called math.frexp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['frexp'](...)
    print("\x1b[33mresult of call", "math.frexp", res, "\x1b[36m")
    return res
end
l.math["log"] = function(...)
    print('called math.log(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['log'](...)
    print("\x1b[33mresult of call", "math.log", res, "\x1b[36m")
    return res
end
l.math["tanh"] = function(...)
    print('called math.tanh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['tanh'](...)
    print("\x1b[33mresult of call", "math.tanh", res, "\x1b[36m")
    return res
end
l.math["exp"] = function(...)
    print('called math.exp(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['exp'](...)
    print("\x1b[33mresult of call", "math.exp", res, "\x1b[36m")
    return res
end
l.math["modf"] = function(...)
    print('called math.modf(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['modf'](...)
    print("\x1b[33mresult of call", "math.modf", res, "\x1b[36m")
    return res
end
l.math["cosh"] = function(...)
    print('called math.cosh(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['cosh'](...)
    print("\x1b[33mresult of call", "math.cosh", res, "\x1b[36m")
    return res
end
l.math["asin"] = function(...)
    print('called math.asin(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['asin'](...)
    print("\x1b[33mresult of call", "math.asin", res, "\x1b[36m")
    return res
end
l.math["rad"] = function(...)
    print('called math.rad(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = math['rad'](...)
    print("\x1b[33mresult of call", "math.rad", res, "\x1b[36m")
    return res
end
l.rawset = function(...)
    print('called rawset(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = rawset(...)
    print("\x1b[33mresult of call", "rawset", res, "\x1b[36m")
    return res
end
l.os = {}
l.os["execute"] = function(...)
    print('called os.execute(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['execute'](...)
    print("\x1b[33mresult of call", "os.execute", res, "\x1b[36m")
    return res
end
l.os["rename"] = function(...)
    print('called os.rename(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['rename'](...)
    print("\x1b[33mresult of call", "os.rename", res, "\x1b[36m")
    return res
end
l.os["setlocale"] = function(...)
    print('called os.setlocale(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['setlocale'](...)
    print("\x1b[33mresult of call", "os.setlocale", res, "\x1b[36m")
    return res
end
l.os["getenv"] = function(...)
    print('called os.getenv(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['getenv'](...)
    print("\x1b[33mresult of call", "os.getenv", res, "\x1b[36m")
    return res
end
l.os["difftime"] = function(...)
    print('called os.difftime(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['difftime'](...)
    print("\x1b[33mresult of call", "os.difftime", res, "\x1b[36m")
    return res
end
l.os["remove"] = function(...)
    print('called os.remove(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['remove'](...)
    print("\x1b[33mresult of call", "os.remove", res, "\x1b[36m")
    return res
end
l.os["date"] = function(...)
    print('called os.date(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['date'](...)
    print("\x1b[33mresult of call", "os.date", res, "\x1b[36m")
    return res
end
l.os["exit"] = function(...)
    print('called os.exit(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['exit'](...)
    print("\x1b[33mresult of call", "os.exit", res, "\x1b[36m")
    return res
end
l.os["time"] = function(...)
    print('called os.time(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['time'](...)
    print("\x1b[33mresult of call", "os.time", res, "\x1b[36m")
    return res
end
l.os["clock"] = function(...)
    print('called os.clock(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['clock'](...)
    print("\x1b[33mresult of call", "os.clock", res, "\x1b[36m")
    return res
end
l.os["tmpname"] = function(...)
    print('called os.tmpname(\x1b[35m'..table.concat({...}, ", ")..'\x1b[36m)')
    local res = os['tmpname'](...)
    print("\x1b[33mresult of call", "os.tmpname", res, "\x1b[36m")
    return res
end
return l