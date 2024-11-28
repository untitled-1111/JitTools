return function(jit)
    
    local dumper = {}

    dumper.dumpFuncWithRandomName = function(func)
        local scriptDir = debug.getinfo(1, "S").source:match("@(.*[\\/])")
        local fileName = scriptDir.. "dumps\\" .. math.random(0, 50000) .. ".txt"
        local f1 = io.open(fileName, "wb")
        jit.dump(func, f1, true)
        f1:close();
        print("\x1b[35m[DUMPER] \x1b[37mDumped func: ", func, "in", fileName, "\x1b[36m")
    end

    dumper.dumpFunc = function(func, fileName)
        local f1 = io.open(fileName, "wb")
        jit.dump(func, f1, true)
        f1:close();
        print("\x1b[35m[DUMPER] \x1b[37mDumped func: ", func, "in", fileName, "\x1b[36m")
    end

    return dumper
end