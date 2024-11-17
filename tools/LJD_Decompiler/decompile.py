import os
import sys
import pathlib

if __name__ == "__main__":
    script = pathlib.Path(sys.argv[1]).absolute()
    filedata = script.read_bytes()

    if filedata[:3] == b'\x1BLJ':
        bcver = int(filedata[3])

        if bcver == 1 or bcver == 2:
            ljver = '2.' + str(bcver - 1)
            print('Determined LuaJIT bytecode version:', ljver)

        os.system('python main.py --enable_logging --catch_asserts --file="{0}" --output="{1}-decompiled.lua"'.format(script, os.path.splitext(script)[0]))
    else:
        print('Invalid LuaJIT bytecode')

    os.system('pause')