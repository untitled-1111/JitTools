local ffi = require('ffi')

local custom_GMeta = {}
local _getmetatable = getmetatable
local _setmetatable = setmetatable
local _rawset = rawset
local _rawget = rawget

setmetatableWrapper = function(object, meta)
    _rawset(custom_GMeta, object, object)
    return _setmetatable(object, meta)
end

setmetatable = function(tab, meta)
    print("call setmetatable")
    if tab == _G then
        local meta_G = _getmetatable(_G)
        if not meta then meta = {} end
        local _meta__Index = meta.__index

        meta.__index = function(self, key)
            local value = meta_G.__index(self, key)
            if type(value) == "function" and type(_meta__Index) == "function" then
                return _meta__Index(self, key)
            end
            return value
        end
        _setmetatable(_G, meta)
    else
        if _rawget(custom_GMeta, tab) then
            _rawset(custom_GMeta, tab, nil)
        end
        return _setmetatable(tab, meta)
    end
end

local searchLocalMT = function(object)
    for key, value in pairs(custom_GMeta) do
        if value == object then
            return true
        end
    end
    return false
end

getmetatable = function(object)
    print('call getmetatable')
    if searchLocalMT(object) then
        return nil
    end
    return _getmetatable(object)
end

rawset = function(tab, index, value)
    print("call rawset", index, value)
    tab[index] = value
    return tab
end

rawget = function(tab, index)
    print("call rawget")
    return tab[index]
end

rawlen = function(v)
    print("call rawlen")
    return #v
end

rawequal = function(v1, v2)
    print("call rawequal", v1, v2)
    return v1 == v2
end

local nopFfi = _setmetatable({
    new = function(...)
        print('call unsafe ffi.new')
        return ffi.new(...)
    end,
    string = function(...)
        print('call unsafe ffi.string')
        return ffi.string(...)
    end
}, {
    __index = function(self, key)
        print('call ffi.' .. tostring(key))
        return function() end
    end
})

package = setmetatableWrapper({}, {
    __index = function(self, key)
        print('call package.' .. tostring(key))
        return function() end
    end
})

require = function(lib)
    print('call require ' .. tostring(lib))

    if lib == 'ffi' then
        return nopFfi
    end
end

os = setmetatableWrapper({
    execute = function() print("call os.execute") end,
    exit = function() print("call os.exit") end,
    remove = function() print("call os.remove") end,
    rename = function() print("call os.rename") end,
}, {
    __index = os
})

io = setmetatableWrapper({}, {
    __index = function(self, key)
        print('call io.' .. tostring(key))
        return function() end
    end
})

error = function(message, level)
    print('call error', message, level)
end

debug = setmetatableWrapper({
    getinfo = function()
        print("call debug.getinfo")
        return false
    end
}, {
    __index = function(self, key)
        print('call debug.' .. tostring(key))
        return function() end
    end
})

--FIXME:
local _error = error
string = setmetatableWrapper({
    dump = function(...)
        return _error('unable to dump given function')
    end
}, {
    __index = string
})

load = function(code)
    load_call(code)
    return function() end
end

loadstring = function(code)
    loadstring_call(code)
    return function() end
end

loadfile = function(filename)
    print('call loadfile ' .. tostring(filename))
    return function() end
end

dofile = function(filename)
    print('call dofile ' .. tostring(filename))
    return function() end
end

getWorkingDirectory = function()
    print('call getWorkingDirectory', arg[1])
    return "moonloader\\" .. arg[1]
end

thisScript = setmetatableWrapper({
    path = "moonloader\\" .. arg[1],
    filename = arg[1]
}, {
    __index = function(self, key)
        print('call script.this.' .. tostring(key))
        return function() end
    end,
    __call = function()
        return thisScript
    end
})

script = setmetatableWrapper({
    this = thisScript,
}, {
    __index = function(self, key)
        print('call script.' .. tostring(key))
        return function() end
    end
})

local _pcall = pcall
pcall = function(func, ...)
    if func == require then
        return false, "module '" .. ... .. "' not found:"
    else
        return _pcall(func, ...)
    end
end

local copyMT = {}
local copy = _setmetatable({}, copyMT)
copyMT.__call = function(self, obj, seen)
    if type(obj) ~= 'table' then return obj end
    if seen and seen[obj] then return seen[obj] end
    local s = seen or {}
    local res = _setmetatable({}, _getmetatable(obj))
    s[obj] = res
    for k, v in pairs(obj) do res[copy(k, s)] = copy(v, s) end
    return res
end

local localG = copy(_G)
_setmetatable(_G, {
    __index = function(self, key)
        if _rawget(localG, key) then
            print("_G remove trap", key)
            return nil
        end
        print('call unknown _G: ' .. tostring(key))
        return function() end
    end
})
