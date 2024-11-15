local l = {}

local function register_function(name, callback)
    local tab = {}
    setmetatable(tab, {
        __index = function(self, i)
            local res = rawget(self, i)
            if res == nil then
                rawset(self, i, register_function(name .. '.' .. i))
                res = rawget(self, i)
            end
            return res
        end,
        __call = function(self, ...)
            print('hooked ' .. name .. '(' .. table.concat({...}, ', ') .. ')')
            return callback(...)
        end
    })

    return tab
end

setmetatable(l, { __index = function(self, i)
    local res = rawget(self, i)
    if res == nil then
        rawset(self, i, register_function(i, function()
            return true
        end))
        res = rawget(self, i)
    end
    return res
end })

-- чтобы не обходили метаметоды через rawget
l.rawget = function(t, i)
    if t == l then return t[i] end
    return rawget(t, i) -- во избежения stack overflow в других метатаблицах
end

-- чтобы не убрал таблицу с метаметодами
l.setmetatable = function(t, mt)
    if t == l then return end
    return setmetatable(t, mt)
end

l.getmetatable = function(t, mt)
    if t == l then return end
    return getmetatable(t, mt)
end

return l