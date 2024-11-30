local ffi = require 'ffi'
local ins = require "inspect"
ffi.cdef[[

int SetConsoleTitleA(const char* name);

typedef const char *LPCSTR;
typedef LPCSTR LPCTSTR;
typedef uint32_t DWORD;

int PlaySound(
   LPCTSTR pszSound,
   int     hmod,
   DWORD   fdwSound
);

]]

function getFileNameFromPath(path)
    return string.match(path, '.+\\(.-)$')
end
function getFileNameFromPathWithoutEx(path)
    return string.match(path, '.+\\(.+)%..+$')
end
targetName = getFileNameFromPath(arg[1])
os.setlocale('Russian')
ffi.C.SetConsoleTitleA("Lua Runtime Checker")
local orig_require = require

math.randomseed(os.time())
os.execute('color 3')
os.execute('cls')

print("\x1b[35m[SYSTEM] \x1b[37m> Запуск инструмента..", getFileNameFromPath(arg[1]))

local registry = debug.getregistry()

local jit = require 'jit.bc'
local dumper = require("LRCDumper")(jit)

local function buildProxyFuncs()

    local code = io.open("LRCFuncs.lua", "rb"):read("*a"); --получение кода скрипта
    local proxyInit = loadstring(code) -- попытка загрузить его

    if proxyInit then
        
        local proxyDebug = {}

        local debug = {
            counter = 0,
            destoyed = 0
        }
        
        for k, v in pairs(registry['_LOADED']['debug']) do debug.counter = debug.counter + 1 end

        if debug.counter == 18 then

            for k, v in pairs(registry['_LOADED']['debug']) do debug[k] = v; end
            --print("\x1b[33m[D] \x1b[37mSaved, prepared to use. V:", debug.counter, "\x1b[36m")

        else
            print("\x1b[33m[D] \x1b[37mНе сохранено, обнаружено нарушение. V:", debug.counter, "\x1b[36m")
        end
        
        for k, v in pairs(registry['_LOADED']['debug']) do

            proxyDebug[k] = function(...) 
                print("\x1b[33m[D] \x1b[37mЛовушка запущена. Тип:", k, ..., "\x1b[36m"); 
                return false
            end

            debug.destoyed = debug.destoyed + 1 
        end

        --print("\x1b[33m[D] \x1b[37mDestroyed V:", debug.destoyed, "\x1b[36m")

        local fin = proxyInit()

        fin["debug"] = proxyDebug
        fin["_G"] = fin

        return fin
    end

    return {}
end

local code = io.open(arg[1], "rb"):read("*a"); 
local scriptInit = loadstring(code) 

if scriptInit ~= nil then 

    local metatab = setmetatable(buildProxyFuncs(), {
        __index = function(self, index, another) 
            print("\x1b[35m[SYSTEM] \x1b[37mОбнаружен пустой индекс", index, "\x1b[36m")
            print("\x1b[35m[SYSTEM] \x1b[37mУстановка метатаблицы индексу", index, "\x1b[36m")

            local mt = {}

            local thisFunc = debug.getinfo(1, "f").func
            mt = setmetatable(buildProxyFuncs(), {
                __add = thisFunc,
                __sub = thisFunc,
                __mul = thisFunc,
                __div = thisFunc,
                __mod = thisFunc,
                __unm = thisFunc,
                __concat = thisFunc,
                __eq = thisFunc,
                __lt = thisFunc,
                __le = thisFunc,
                __call = function(self, ...)
                    print("")
                    print("\x1b[33m[META] \x1b[37mВызван метаметод индекса:", index, "\x1b[36m") 
                    print("\x1b[33m[META] \x1b[37mФункция", index, "вызвана с такими параметрами:\x1b[36m")
    
                    local params = {unpack({...})}

                    print("\x1b[33m[META]", ins(params), "\x1b[36m")

                    for k, v in pairs(params) do
                        if type(v) == "table" then
    
                            print("\x1b[33m[META] \x1b[37m", ins(v), "\x1b[36m")
    
                        elseif type(v) == "function" then
    
                            for i = 0, 3 do 
                                local a, b = debug.getupvalue(v, i)
                                if a ~= nil then
                                    print("\x1b[33m[META] \x1b[37mПолучение информации о функции", i, type(b), "\x1b[36m")
                                    if type(b) == "table" then
                                        print("\x1b[33m[META] \x1b[37ml", ins(b), "\x1b[36m")
                                    else
                                        print("\x1b[33m[META] \x1b[37ml", b, "\x1b[36m")
                                    end
                                end
                            end
    
                        else
    
                            print("\x1b[33m[META] \x1b[37m", type(v), v, "\x1b[36m")
    
                        end
                    end
					return mt
                end,
                __index = thisFunc
            })
			if type(self) == "table" then
				rawset(self, index, mt) 
				return mt
			end
    end,
    __newindex = function(self, index, value)
        print("")
        print("\x1b[33m[META] \x1b[37mНовый элемент в _G обнаружен:", index, value, "\x1b[36m")
        rawset(self, index, value)

        if type(value) == "function" then
            dumper.dumpFunc(value, "dumps\\" .. getFileNameFromPathWithoutEx(arg[1]) .. "." .. index .. ".txt")

            for i = 0, 3 do 
                local a, b = debug.getupvalue(value, i)
                if a ~= nil then
                    print("\x1b[33m[META] \x1b[37mПолучение информации о функции", i, type(b), "\x1b[36m")
                    if type(b) == "table" then
                        print("\x1b[33m[META] \x1b[37ml", ins(b), "\x1b[36m")
                    else
                        print("\x1b[33m[META] \x1b[37ml", b, "\x1b[36m")
                    end
                end
            end
        elseif type(value) == "table" then
            print("\x1b[33m[META] \x1b[37mПолучение информации о таблице", "\x1b[36m")
            print(ins(value)) -- ку ку
        end

        io.read()
        --debug.debug()
      end,
    })

    setfenv(scriptInit, metatab)
    local errorHandler = function(error)
        print("\x1b[31m[ERROR] \x1b[37m", error)
        local fName = string.match(error, "attempt to call global '(.-)'")
        if fName then
            print("\x1b[33m[META] \x1b[37mНевалидный вызов функции. Установка патча и перезапуск скрипта..", "\x1b[36m")
            metatab[fName] = function() print("\x1b[35m[SYSTEM] \x1b[37mВызвана временная функция "..fName.."\x1b[36m") end
            setfenv(scriptInit, metatab)
            xpcall(scriptInit, debug.getinfo(1, "f").func)
        end
    end
    
    print("\x1b[35m[SYSTEM] \x1b[37mИнициализация скрипта\x1b[36m")
    xpcall(scriptInit, errorHandler)
    print("\x1b[35m[SYSTEM] \x1b[37mСкрипт загружен. Выполнение пользовательских команд\x1b[36m")

    local main = ({getfenv(scriptInit)})[1]["main"]

    if main then
        if type(main) == "function" then
            print("\x1b[35m[SYSTEM] \x1b[37mВызов точки входа мунлоадера\x1b[36m")
            main()
        end
    end

end