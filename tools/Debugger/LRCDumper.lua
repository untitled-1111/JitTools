return function(jit)
    
    local dumper = {}

    dumper.dumpFunc = function(func, fileName)
        local f1 = io.open(fileName, "wb")
        jit.dump(func, f1, true)
        f1:close();
        print("\x1b[35m[DUMPER] \x1b[37mDumped func: ", func, "in", fileName, "\x1b[36m")
    end

    dumper.dumpFuncWithRandomName = function(func)
        local fileName = "dumps\\" .. math.random(0, 50000) .. ".txt"
        local f1 = io.open(fileName, "wb")
        jit.dump(func, f1, true)
        f1:close();
        print("\x1b[35m[DUMPER] \x1b[37mDumped func: ", func, "in", fileName, "\x1b[36m")
    end

    return dumper
end