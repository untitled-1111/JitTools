"""

     ▄█  ▄█      ███                                    
    ███ ███  ▀█████████▄                                
    ███ ███▌    ▀███▀▀██                                
    ███ ███▌     ███   ▀                                
    ███ ███▌     ███                                    
    ███ ███      ███                                    
    ███ ███      ███                                    
█▄ ▄███ █▀      ▄████▀                                  
▀▀▀▀▀▀                                                  
    ███      ▄██████▄   ▄██████▄   ▄█          ▄████████
▀█████████▄ ███    ███ ███    ███ ███         ███    ███
   ▀███▀▀██ ███    ███ ███    ███ ███         ███    █▀ 
    ███   ▀ ███    ███ ███    ███ ███         ███       
    ███     ███    ███ ███    ███ ███       ▀███████████
    ███     ███    ███ ███    ███ ███                ███
    ███     ███    ███ ███    ███ ███▌    ▄    ▄█    ███
   ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██  ▄████████▀ 
                                  ▀                    
"""

import os
import sys
import pathlib
import re
import ctypes
import subprocess
import codecs
import random
import tkinter as tk
from tkinter import filedialog
import socket
from requests import get

try:
    class EncodedEntry:
        def __init__(self, bytes, start, end):
            self.bytes = bytes
            self.start = start
            self.end = end

        def decode(self):
            if self.bytes[0] != len(self.bytes):
                return None
            bytes_decoded = [
                (0xff - ((byte - index - 1) & 0xff)) & 0xff
                for index, byte in enumerate(self.bytes[1:])
            ]
            try:
                return codecs.decode(bytes(bytes_decoded), 'windows-1251')
            except Exception:
                return None

        def decode2(self):
            if len(self.bytes) < 11:
                return None
            bytes_decoded = [
                (0xff - (byte & 0xff)) & 0xff
                for index, (byte, a) in enumerate(zip(self.bytes[11:], range(11 + self.bytes[10] - self.bytes[0])))
            ]
            try:
                return codecs.decode(bytes(bytes_decoded), 'windows-1251')
            except Exception:
                return None

    def read_file(name):
        with open(name, 'rb') as file:
            return file.read()

    def write_file(name, cont):
        with open(name, 'wb') as file:
            file.write(cont)

    def hexdump(var):
        return var.hex(sep=' ').upper()

    def unhexdump(var):
        import codecs
        return codecs.decode(var, 'hex')

    ret_opcodes = [0x49, 0x4A, 0x4B, 0x4C, 0x43, 0x44]

    def opcode_info(data, pos):
        return data[pos], data[pos + 3] >= 128, read_uint16(data[pos + 2 : pos + 4])

    def new_dist(offset, dist):
        opcode_pos = offset // 4
        return (opcode_pos + dist + 1) * 4

    def gui(file_path):
        try: 
            root.title(f"JitTools GUI v{version}")
            root.configure(bg='#212121')
            label_color = '#76d6ae'
            button_color = '#2E865F'

            root.wm_state("zoomed")

            buttons = [
                "Unhider", "Full Unprotector", "LJD Decompiler", "Decompiler + ASM", "Debugger",
                "Hook Obfuscation", "Shit Deobfuscation", "XOR Unpacker", "Moonsec Dumper",
                "Compiler + Decompiler (DEBUG)", "Compiler", "Script Joiner", "Luad"
            ]

            for idx, button_text in enumerate(buttons, start=1):
                button = tk.Button(root, text=f"[{idx}] {button_text}", font=("Consolas", 14), fg=button_color, bg='#333333', relief=tk.FLAT, highlightthickness=0, activebackground='#444444', activeforeground=button_color)

                def on_enter(e, button=button):
                    button.config(bg='#444444')

                def on_leave(e, button=button):
                    button.config(bg='#333333')

                def gui_button_function(e, button_text=button_text):
                    if button_text == "Unhider":
                        unhider_btn(file_path)
                    elif button_text == "Full Unprotector":
                        fullunprotector_btn(file_path)
                    elif button_text == "LJD Decompiler":
                        ljd_decompiler(file_path)
                    elif button_text == "Decompiler + ASM":
                        Decompilerasm_btn(file_path)
                    elif button_text == "Debugger":
                        debugger_btn(file_path)
                    elif button_text == "Hook Obfuscation":
                        hookobfuscation_btn(file_path)
                    elif button_text == "Shit Deobfuscation":
                        shitdeobfuscation_btn(file_path)
                    elif button_text == "XOR Unpacker":
                        xorunpacker_btn(file_path)
                    elif button_text == "Moonsec Dumper":
                        moonsecdumper_btn(file_path)
                    elif button_text == "Compiler + Decompiler (DEBUG)":
                        compilerDecompilerdebug_btn(file_path)
                    elif button_text == "Compiler":
                        compiler_btn(file_path)
                    elif button_text == "Script Joiner":
                        scriptjoiner_btn(file_path)
                    elif button_text == "Luad":
                        luad_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', 'Luad', 'build', 'bin', 'Release', 'luad.exe')
                        subprocess.Popen([luad_path])
                        
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)
                button.bind("<Button-1>", gui_button_function)

                button.place(relx=0.5, rely=0.23 + 0.052 * idx, anchor=tk.CENTER)

            label = tk.Label(root, text=f"JitTools - {os.path.basename(file_path)}", font=("Consolas", 18), fg=label_color, bg='#212121')
            label.place(relx=0.5, rely=0.10, anchor=tk.CENTER)

            tools_info = tk.Label(root, text="информация об инструментах", font=("Consolas", 12, "underline"), fg="#ffffff", bg="#212121", cursor="hand2")
            tools_info.place(relx=0.5, rely=0.14, anchor=tk.CENTER)
            tools_info.bind("<Button-1>", lambda e: tk.messagebox.showinfo("Информация", """Описание инструментов:

Unhider - раскрывает скрытые функции, если они имеются

Full Unprotector - содержит в себе два инструмента для снятия защиты до декомпиляции

LJD Decompiler - позволяет декомпилировать скрипт в читаемый код (форк LJD)

Decompiler + ASM - позволяет декомпилировать скрипт в читаемый код, а также сохраняет псевдо-ASM

Debugger - получает дампы функций, выполняя код скрипта на вашем ПК

Hook Obfuscation - позволяет получить код скрипта из под обфускации, выполняя его на вашем ПК

Shit Deobfuscation - снимает один из обфускаторов

XOR Unpacker - позволяет распаковать скрипт, зашифрованный при помощи XOR
                                                                        
Moonsec Dumper - дампер всего скрипта, благодаря которому можно раскрыть популярный Moonsec, выполняет код на вашем ПК

Compiler + Decompiler [DEBUG] - позволяет получить полезную информацию о скрипте, компилируя и декомпилируя его с дебаг параметрами
                                                                           
Compiler - обычный компилятор LuaJIT

Script Joiner - позволяет соединить два скрипта в один, например для подделки переменной
                                                                        
Luad - позволяет просмотреть байт-код скрипта, имеет другие функции"""))
            link = tk.Label(root, text="тема на blasthack", font=("Consolas", 12, "underline"), fg="#ffffff", bg="#212121", cursor="hand2")
            link.place(relx=0.5, rely=0.17, anchor=tk.CENTER)
            link.bind("<Button-1>", lambda e: os.startfile("https://www.blast.hk/threads/223498/"))

            root.mainloop()

        except Exception as e:
            print(f"[GUI] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def moonsecdumper_btn(file_path):
        try:
            result = tk.messagebox.askyesno("Moonsec Dumper", "[!] Dumper открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                            "Его необходимо использовать в изолированном пространстве.\n"
                                            "Вы уверены, что хотите открыть Dumper? (да/нет)")
            
            if result:
                
                private_roflan = """local function MoonSecHook()
  
  local anti_tamper = string.match
  local unpack_orig = table.unpack

  string.match = function(a,b) -- // moonsec anti-tumper
    if b == ('%d+') then
      return '1'
    elseif b == (':%d+: a') then
      return (':1: a')
    end
    return anti_tamper(a,b)
  end

  function debugInfo(file, string)
    local file = io.open(file, 'a')  
    if file then
      file:write(string .. '\\n')  
      file:close()  
    end
  end

    local patches = {
        require = function(original)
            return function(v)
                print('[require] ' .. v)
        debugInfo('require.txt', v)
                return original(v)
            end
        end,

        exit = function(original)
            return function(code)
                print('[os.exit] ' .. tostring(code))
            end
        end,

        error = function(original)
            return function(msg, level)
                local funcName = debug.getinfo(2, 'n') and debug.getinfo(2, 'n').name or 'unknown'
                print('[' .. funcName .. '] ' .. tostring(msg))
            end
        end
    }

    for name, patch in pairs(patches) do
        local original_function = _G[name]  
        if original_function then
            _G[name] = patch(original_function)  
        end
    end

  local function wrapFunction(func, name)
    return function(...)
      local info = debug.getinfo(func, 'S')
      if info and info.source then
        local string = '[FUNCTION CALL] Функция: ' .. name .. ' Код: ' .. info.source
        debugInfo('function_call.txt', string) 
      end
      return func(...)
    end
  end

    local originalGlobals = _G 

    setmetatable(_G, {
    __index = function(t, key)
            local value = rawget(originalGlobals, key)
            if value ~= nil then
                return value 
            end
            return nil  
        end,

        __index = function(t, key)
            local value = rawget(originalGlobals, key)
            if type(value) == 'function' then
                print('[GET FUNC]: ' .. tostring(key))
                return wrapFunction(value, tostring(key))
            end
            return value
        end,

        __newindex = function(t, key, value)
            if type(value) == 'function' then
                local string = '[FUNCTION DUMPER] Создана функция: ' .. tostring(key)
                debugInfo('functions.txt', string) 
                rawset(t, key, wrapFunction(value, tostring(key)))  
            elseif type(value) == 'table' then
                local string = '[TABLE DUMPER] Создана таблица: ' .. tostring(key)
                debugInfo('tables.txt', string)  
                rawset(t, key, value) 
            else
                local string = '[VARIABLE SET] Переменная: ' .. tostring(key) .. ' = ' .. tostring(value)
                debugInfo('variables.txt', string)  
                rawset(t, key, value)  
            end
        end
    });
  
  local function table_to_string(tbl)
    local str = '['
    for k, v in pairs(tbl) do
      if type(v) == 'table' then
        str = str .. table_to_string(v)
      else
        str = str .. string.format('\\n[Key: %s] -> [Val: %s], ', tostring(k), tostring(v))
      end
    end
    return str:sub(1, -3) .. '\\n],\\n'
  end
  
  local function iterate_and_log(tbl)
    if type(tbl) == 'table' then
      for k, v in pairs(tbl) do
        if type(v) == 'table' then
          debugInfo('dump.txt', table_to_string(v) .. '\\n')
        else
          debugInfo('dump.txt', string.format('{Key: %s | Val: %s}\\n', tostring(k), tostring(v)))
        end
      end
    end
  end
  
  function unpack(...)
    local res = {unpack_orig(...)}
    if type(res[1]) == 'table' then
      iterate_and_log(res[1])
    end
    return unpack_orig(...)
  end

  print('[MOONSEC-DUMPER] HOOKS INSTALLED =)')  
end

MoonSecHook();"""
                with open(file_path, 'r+b') as file:
                    content = file.read()
                    try:
                        file_content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        file_content = content.decode('cp1251')
                    file.seek(0)
                    file.write((private_roflan + file_content).encode('utf-8'))

                file_path_abs = os.path.abspath(file_path)
                subprocess.run([
                                os.path.join(os.path.dirname(file_path_abs), 'tools', 'Debugger', 'luajit.exe'),
                                file_path_abs
                ], check=True)

                tk.messagebox.showinfo("Dumper", f"Дампы успешно сохранены в папку: {os.path.dirname(file_path)}")
                

            else:
                gui(file_path)
                

        except Exception as e:
            print(f"[Moonsec Dumper] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def unhider_btn(file_path):
        try: 
            script_luajit = LuaJIT_two(file_path)
            basename = os.path.basename(file_path)

            fn = os.path.splitext(file_path)
            save_to = f"{fn} - JTools (UH).lua"
            saved_as = os.path.basename(save_to)

            if not script_luajit.isCompiled():
                tk.messagebox.showerror("Unhider", f"{basename} не является скомпилированным LuaJIT скриптом.")
            else:
                protos = script_luajit.protos()
                if not len(protos):
                    tk.messagebox.showerror("Unhider", f"{basename} не имеет прототипов.")
                else:
                    count, amount = unhide_funcs(script_luajit)
                    fn = os.path.splitext(script_luajit.path)
                    if count > 0:
                        pathlib.Path(save_to).write_bytes(script_luajit.data)
                        result = tk.messagebox.askyesno("Unhider", f"Успешно сохранено в файл: {saved_as} ({count} / {amount})\nОткрыть папку с файлом? (да/нет)")
                        if result:
                            os.startfile(os.path.dirname(save_to))

                        gui(file_path)
                    else:
                        tk.messagebox.showerror("Unhider", f"В файле {basename} нету скрытых функций.")

        except Exception as e:
            print(f"[UNHIDER] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def fullunprotector_btn(file_path):
        try: 
            basename = os.path.basename(file_path)
            script_luajit = LuaJIT(file_path)

            if not script_luajit.isCompiled():
                tk.messagebox.showerror("Unprot", f"{basename} не является скомпилированным LuaJIT скриптом.")

            else:
                script = hexdump(read_file(file_path))
                pattern = r'(30\s+\d+\s+\d+\s+\d+\s+)(40\s+\d+\s+\d+\s+\d+)(\s+51\s+\d+\s+\d+\s+\d+)'
                replacement = r'\g<1>54 00 00 80\g<3>'
                find_opcode = re.sub(pattern, replacement, script)
                final_script = unhexdump(find_opcode.replace(' ', ''))

                fn, ext = os.path.splitext(file_path)
                save_to = f"{fn} - JTools (BP){ext}"

                if len(final_script) != len(script):
                    write_file(save_to, final_script)
                else:
                    tk.messagebox.showerror("Bypass", "Не обнаружено защиты в скрипте.")
        
                    # check_file()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                    root.deiconify()
                    if not file_path:
                        sys.exit()
                    gui(file_path)

                for filename in parse_files():
                    script = LuaJIT(filename)
                    basename = os.path.basename(filename)
                    fn, ext = os.path.splitext(script.path)
                    save_to = f"{fn} - JTools (UP){ext}"
                    saved_as = os.path.basename(save_to)

                    if not script.isCompiled():
                        print(f"ERROR: {basename} is not a LuaJIT-compiled script")
                        continue
                    protos = script.get_protos()
                    proto_num = 0
                    for proto in reversed(protos):
                        proto_start = proto["ins"]
                        proto_end = proto_start + proto["numbc"] * 4 
                        proto_data = script.data[proto_start : proto_end]
                        jump_off, trash_opcodes, jump_max = 0, 0, 0
                        
                        while True:
                            opcode = proto_data[jump_off]
                            if opcode == 0x12:
                                jump_off += 4
                                trash_opcodes += 1
                                continue
                            if opcode == 0x58 or opcode == 0x32:
                                jmp_dist = read_uint16(proto_data[jump_off + 2 : jump_off + 4]) + 1
                                trash_opcodes += jmp_dist
                                jump_off += 4 * jmp_dist
                                continue
                            break
                        while True:
                            opcode, jmp_down, uint = opcode_info(proto_data, jump_off)
                            if opcode == 0x32 or (opcode == 0x58 and jmp_down):
                                tmp = new_dist(jump_off, uint)
                                if len(proto_data) > tmp > jump_max: jump_max = tmp
                                jump_off += 4
                                continue
                            if opcode in ret_opcodes:
                                if jump_off < jump_max:
                                    jump_off += 4
                                    continue
                                script.data[proto_start + jump_off + 4 : proto_end] = []
                                script.data[proto_start : proto_start + trash_opcodes * 4] = []
                                total_opcodes = proto["numbc"] - (jump_off // 4 - trash_opcodes) - 1
                                
                                # updating number of opcodes
                                numbc_pos = proto["numbc_pos"]
                                length = proto["numbc_length"]     
                                script.data[numbc_pos : numbc_pos + length], new_length = write_uleb128(proto["numbc"] - total_opcodes)
                                
                                extra_length = 0
                                if new_length < length:
                                    extra_length = new_length - length
                                
                                # updating prototype size
                                proto_pos = proto["pos"]
                                proto_size, length = read_uleb128(script.data[proto_pos:])
                                script.data[proto_pos : proto_pos + length], _ = write_uleb128(proto_size - (total_opcodes * 4) + extra_length)
                                break            
                            jump_off += 4
                            continue   
                        proto_num += 1
                    pathlib.Path(save_to).write_bytes(script.data)
                    result = tk.messagebox.askyesno("Unprot & Bypass", f"Успешно сохранено в папку: {os.path.dirname(save_to)}\nОткрыть её? (да/нет)")
                    
                    # check_file()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                    root.deiconify()
                    if not file_path:
                        sys.exit()
                    gui(file_path)

                    if result:
                        os.startfile(os.path.dirname(save_to))
                    else:
                        gui(file_path)

        except Exception as e:
            print(f"[FULL UNPROT] {str(e)}")
            print(f"[FULL UNPROT] Ошибка в строке {sys.exc_info()[-1].tb_lineno}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def ljd_decompiler(file_path):
        try: 
            luajit_script = LuaJIT_two(file_path)
            file_name = os.path.basename(file_path)
            file_path_abs = os.path.abspath(file_path)
            if not luajit_script.isCompiled():
                tk.messagebox.showerror("Decompiler", f"{file_name} не является скомпилированным LuaJIT скриптом.")
                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.exit()
                gui(file_path)

            else: 
                
                output_file = f"{os.path.dirname(os.path.realpath(__file__))}\\{os.path.splitext(os.path.basename(file_path))[0]} - JTools (LJD_DEC).lua"
                os.system(f'python "{os.path.dirname(os.path.realpath(__file__))}\\tools\\LJD_Decompiler\\main.py"'
                    f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
                    f' --output="{output_file}"')    

                result = tk.messagebox.askyesno("Decompiler", f"Файл успешно сохранен в папке: {os.path.dirname(output_file)}\nОткрыть её? (да/нет)")

                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.exit()
                gui(file_path)

                if result:
                    os.startfile(os.path.dirname(output_file))

                else:
                    gui(file_path)

        except Exception as e:
            print(f"[Decompiler] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def Decompilerasm_btn(file_path):
        try: 
            luajit_script = LuaJIT_two(file_path)
            file_name = os.path.basename(file_path)
            file_path_abs = os.path.abspath(file_path)
            if not luajit_script.isCompiled():
                tk.messagebox.showerror("Decompiler + ASM", f"{file_name} не является скомпилированным LuaJIT скриптом.")
                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.exit()
                gui(file_path)

            else: 
                result = tk.messagebox.askyesno("Decompiler + ASM", "[!] ASM открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                               "Его необходимо использовать в изолированном пространстве.\n"
                                               "Вы уверены, что хотите открыть ASM? (да/нет)")

                if result:
                    
                    output_file = f"{os.path.dirname(os.path.realpath(__file__))}\\{os.path.splitext(os.path.basename(file_path))[0]} - JTools (D).lua"
                    os.system(f'python {os.path.dirname(os.path.realpath(__file__))}\\tools\\Decompiler_and_ASM\\main.py'
                        f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
                        f' --output="{output_file}"')
                    
                    output_file = f"{os.path.dirname(os.path.realpath(__file__))}\\{os.path.splitext(os.path.basename(file_path))[0]} - JTools (ASM).asm"
                    os.system(f'python "{os.path.dirname(os.path.realpath(__file__))}\\tools\\Decompiler_and_ASM\\main.py"'
                            f' --catch_asserts --asm --with-line-numbers --file="{file_path_abs}"'
                            f' > "{output_file}"')

                    result = tk.messagebox.askyesno("Decompiler + ASM", f"Файлы успешно сохраены в папке: {os.path.dirname(output_file)}\nОткрыть её? (да/нет)")
                    
                    
                    # check_file()
                    root.withdraw()
                    file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                    root.deiconify()
                    if not file_path:
                        sys.exit()
                    gui(file_path)

                    if result:
                        os.startfile(os.path.dirname(output_file))

                else:
                    gui(file_path)

        except Exception as e:
            print(f"[Decompiler + ASM] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def debugger_btn(file_path):
        try:
            result = tk.messagebox.askyesno("DEBUGGER", "[!] DEBUGGER открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                                "Его необходимо использовать в изолированном пространстве.\n"
                                                "Вы уверены, что хотите открыть DEBUGGER? (да/нет)")
            if result:
                
                file_path_abs = os.path.abspath(file_path)
                subprocess.run([
                                os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Debugger\\luajit.exe',
                                os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Debugger\\!0LuaRuntimeChecker.lua',
                                file_path_abs
                            ], check=True)

                result = tk.messagebox.askyesno("DEBUGGER", f"Успешно, дампы функций могут находиться в этой папке: {os.path.join(os.path.dirname(file_path_abs), 'dumps')}\nОткрыть её? (да/нет)")
                

                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.exit()
                gui(file_path)

                if result:
                    os.startfile(os.path.join(os.path.dirname(file_path_abs), 'dumps'))
            else:
                gui(file_path)

        except Exception as e:
            print(f"[DEBUGGER] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def hookobfuscation_btn(file_path):
        try:
            result = tk.messagebox.askyesno("HOOK OBFUSCATION", "[!] Hook Obfuscation открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                              "Его необходимо использовать в изолированном пространстве.\n"
                              "Вы уверены, что хотите открыть Hook Obfuscation? (да/нет)\n")

            if result:
                
                file_path_abs = os.path.abspath(file_path)
                subprocess.run([
                    os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Hook Obfuscation\\luajit.exe',
                    os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Hook Obfuscation\\main.lua',
                    file_path_abs
                ], check=True)

                result = tk.messagebox.askyesno("HOOK OBFUSCATION", f"Успешно, итоговые файлы могут находиться в этой папке: {os.path.dirname(os.path.join(os.path.dirname(file_path_abs), 'output'))}\nОткрыть её? (да/нет)")
                
                
                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.exit()
                gui(file_path)

                if result:
                    os.startfile(os.path.join(os.path.dirname(file_path_abs), 'output'))
                    
            else:
                gui(file_path)

        except Exception as e:
            print(f"[HOOK OBFUSCATION] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def shitdeobfuscation_btn(file_path):
        try:
            
            input_file_name, input_file_extension = os.path.splitext(file_path)
            output_file_name = f"{input_file_name} - JTools (SD){input_file_extension}"
            table_re = re.compile(r"(\{[\n\r\t \d,]*?\})")
            number_re = re.compile(r"\d+")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                data = file.read()
            entries = []
            for match in table_re.finditer(data):
                group = match.group(0)
                table = group.replace("\r", "").replace("\n", "").replace("\t", "")

                if table == "{}" or table == "{1}":
                    continue

                bytes_list = [int(num) for num in number_re.findall(table)]
                entries.append(EncodedEntry(bytes_list, match.start(), match.end()))

            offset = 0
            with open(output_file_name, 'w', encoding='utf-8', errors='ignore') as out_file:
                for entry in entries:
                    out_file.write(data[offset:entry.start])
                    val = entry.decode()
                    if val is not None:
                        out_file.write(f"[[{val}]]")
                    else:
                        out_file.write(data[entry.start:entry.end])
                    offset = entry.end
                out_file.write(data[offset:])


            result = tk.messagebox.askquestion("SHIT DEOBFUSCATION", f"Успешно сохранено в файл {os.path.basename(output_file_name)}. Открыть его? (да/нет)")
    
            # check_file()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
            root.deiconify()
            if not file_path:
                sys.exit()
            gui(file_path)

            if result == 'yes':
                os.startfile(output_file_name)
                os.startfile(os.path.dirname(output_file_name))

        except Exception as e:
            print(f"[SHIT DEOBFUSCATION] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def xorunpacker_btn(file_path):
        try:
            result = tk.messagebox.askyesno("XOR Unpacker", "[!] XOR Unpacker открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                              "Его необходимо использовать в изолированном пространстве.\n"
                              "Вы уверены, что хотите открыть XOR Unpacker? (да/нет)\n")

            if result:
                file_path_abs = os.path.abspath(file_path)
                
                subprocess.run([
                    os.path.dirname(os.path.realpath(__file__)) + "\\tools\\XOR_Unpacker\\CLI.exe",
                    file_path_abs
                ], check=True)
                input("Нажмите ENTER для продолжения...")
                
                result = tk.messagebox.askyesno("XOR Unpacker", f"Файл мог быть сохранен в папке: {os.path.dirname(os.path.dirname(os.path.realpath(__file__)) + "\\tools\\XOR_Unpacker")}\nОткрыть её? (да/нет)")
                

                if result:
                    os.startfile(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)) + "\\tools\\XOR_Unpacker")))
                
                # check_file()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
                root.deiconify()
                if not file_path:
                    sys.Иexit()
                gui(file_path)
                    
            else:
                gui(file_path)

        except Exception as e:
            print(f"[XOR Unpacker] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")


    def compiler_btn(file_path):
        try:
            
            script_dir = os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Debugger\\luajit.exe'

            filename, file_extension = os.path.splitext(file_path)
            output_file = f"{filename} - JTools (C).luac"

            subprocess.run([
                script_dir,
                '-b',
                str(file_path),
                output_file
            ], check=True)

            tk.messagebox.showinfo("Compiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
            # check_file()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
            root.deiconify()
            if not file_path:
                sys.exit()
            gui(file_path)

            


        except Exception as e:
            print(f"[Compiler] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def compilerDecompilerdebug_btn(file_path):
        try:
            
            script_dir = os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Debugger\\luajit.exe'
            script_Decompiler_dir = os.path.dirname(os.path.realpath(__file__)) + '\\tools\\Decompiler V2\\luajit-Decompiler-v2.exe'

            filename, file_extension = os.path.splitext(file_path)
            output_file = f"{filename} - JTools (CD){file_extension}"

            subprocess.run([
                script_dir,
                '-bg', str(file_path),
                output_file
            ], check=True)

            subprocess.run([
                script_Decompiler_dir,
                output_file,
                '-o', os.path.dirname(os.path.realpath(__file__)),
                '-u'
            ], check=True)

            tk.messagebox.showinfo("Compiler + Decompiler (DEBUG)", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
            
        
            # check_file()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
            root.deiconify()
            if not file_path:
                sys.exit()
            gui(file_path)

        except Exception as e:
            print(f"[Compiler + Decompiler (DEBUG)] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    def scriptjoiner_btn(file_path):
        try:
            
            root = tk.Tk()
            root.withdraw()  # Close the root window
            file_path = filedialog.askopenfilename(
                title="[SCRIPT JOINER] Выберите файл для склеивания",
                filetypes=[("Lua files", "*.lua;*.luac")]
            )
            if not file_path:
                print("[SCRIPT JOINER] Файл не выбран.")
                sys.exit()

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    data = file.read()

                roflanEbalo = random.randint(1, random.randint(666, 66666666666)) # даже не спрашивайте

                in_result = f"local jittools_rofl_{roflanEbalo} = \""
                in_result += "".join(f"\\x{byte:02X}" for byte in data)
                in_result += f"\"\nloadstring(jittools_rofl_{roflanEbalo})()\n\n"

                output_file_name = f"{os.path.splitext(file_path)[0]} - JTools (SJ){os.path.splitext(file_path)[1]}"
                with open(output_file_name, 'w', encoding='utf-8') as out_file:
                    out_file.write(in_result)

                result = tk.messagebox.askquestion("SCRIPT JOINER", f"Успешно сохранено в файл {os.path.basename(output_file_name)}. Открыть папку с ним? (да/нет)")
                
                
                if result == 'yes':
                    os.startfile(os.path.dirname(output_file_name))

        except Exception as e:
            print(f"[SCRIPT JOINER] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")

    class LuaJIT:
        def __init__(self, path):
            self.path = path
            self.data = bytearray(pathlib.Path(path).read_bytes()) if os.path.exists(path) else None
            self.ok = self.data != None and len(self.data) > 5 and self.data[:3] == b"\x1B\x4C\x4A"

        def exists(self):
            return os.path.exists(self.path)

        def isCompiled(self):
            return self.ok

        def version(self):
            if self.ok:
                return self.data[3]

        def get_proto(self, proto_id):
            return self.get_protos()[proto_id]

        def get_protos(self):
            if not self.ok: return
            protos = []
            i = 5
            while i < len(self.data):
                if self.data[i] == 0:
                    break
                proto, ending = self.pinfo(i)
                protos.append(proto)
                i += ending
            return protos

        def pinfo(self, pos):
            if not self.ok: return None, 0
            size, length = read_uleb128(self.data[pos:])
            proto = {
                "pos": pos,
                "size": size,
                "size_length": length,
                "fullsize": size + length,
                "flags": self.data[pos + length],
                "params": self.data[pos + length + 1],
                "framesize": self.data[pos + length + 2],
                "numuv": self.data[pos + length + 3]
            }
            pos += length + 4
            proto["numkgc"], proto["numkgc_length"] = read_uleb128(self.data[pos:])
            pos += proto["numkgc_length"]
            proto["numkn"], proto["numkn_length"] = read_uleb128(self.data[pos:])
            pos += proto["numkn_length"]
            proto["numbc"], proto["numbc_length"] = read_uleb128(self.data[pos:])
            proto["numbc_pos"] = pos
            proto["ins"] = pos + proto["numbc_length"]

            return proto, proto["fullsize"]

    def read_uleb128(data):
        value = 0
        for i in range(len(data)):
            tmp = data[i] & 0x7f
            value = tmp << (i * 7) | value
            if (data[i] & 0x80) != 0x80:
                break
        return value, i + 1

    def write_uleb128(integer):
        result = bytearray(b'')
        while True:
            byte = integer & 0x7f
            integer >>= 7
            if integer != 0: byte |= 0x80
            result.append(byte)
            if integer == 0: break
        return result, len(result)

    def read_sleb128(value):
        result = 0
        shift = 0
        while True:
            byte = value.shift()
            result |= (byte & 0x7f) << shift
            shift += 7
            if ((0x80 & byte) == 0):
                if shift < 32 and (byte & 0x40) != 0:
                    return result | (~0 << shift)
                return result

    def write_sleb128(integer):
        integer |= 0
        result = bytearray(b'')
        while True:
            byte = integer & 0x7f
            integer >>= 7
            if (integer != 0 and (byte & 0x40)) or (integer == -1 and (byte & 0x40) != 0):
                result.append(byte)
                return result, len(result)
            result.append(byte | 0x80)
        return result, len(result)

    def write_uint16(integer):
        result = bytearray(b'\x00\x80')
        while True:
            byte = integer - 0x100
            if byte >= 0:
                result[1] += 1
                integer -= 0x100
            else:
                result[0] += integer
                break
        return result

    def read_uint16(bytecode):
        hexbc = bytecode.hex()
        integer = bytecode[0]
        byte = bytecode[1] - 0x80
        if byte > 0:
            integer = int(format(byte, 'x') + hexbc[0 : 2], 16)
        return integer

    def file_read(filename):
        if os.path.exists(filename):
            return True, bytearray(pathlib.Path(filename).read_bytes())
        return False, None

    def parse_files():
        files = []
        if len(sys.argv) > 1:
            for i in sys.argv[1:]:
                if os.path.isfile(i) and os.path.exists(i): files.append(i)
                else: print("ERROR: File cannot be found: " + i)
        if not len(files):
            print("ERROR: No file has been chosen")
        return files

    def prompt(Text, Type = ""):
        if Type.lower() == "int" or Type.lower() == "integer":
            return int(input(Text))
        if Type.lower() == "path":
            return input(Text).replace("\"", "")
        return input(Text)

    def unhide_funcs(script):
        count = 0
        protos = script.protos()
        for proto in reversed(protos):
            pos = proto["ins"]
            if script.data[pos : pos + 6] != bytearray(b"\x58\x02\x01\x80\x58\x00"):
                continue
            script.data[pos : pos + 8] = []
            count += 1

            numbc_pos = proto["numbc_pos"]
            length = proto["numbc_length"]
            script.data[numbc_pos : numbc_pos + length], new_length = write_uleb128(proto["numbc"] - 0x02)
            extra_length = 0

            if new_length < length:
                extra_length = length - new_length

            proto_pos = proto["pos"]
            proto_size, length = read_uleb128(script.data[proto_pos:])
            script.data[proto_pos : proto_pos + length], _ = write_uleb128(proto_size - 0x08 - extra_length)
        return count, len(protos)
    
    class LuaJIT_two:
        def __init__(self, path):
            self.path = path
            self.data = bytearray(pathlib.Path(path).read_bytes()) if os.path.exists(path) else None
            self.ok = self.data != None and len(self.data) > 5 and self.data[:3] == b"\x1B\x4C\x4A"

        def exists(self):
            return os.path.exists(self.path)

        def isCompiled(self):
            return self.ok

        def version(self):
            if not self.ok: return "not compiled"
            if self.data[3] == 2: return "2.1"
            if self.data[3] == 1: return "2.0"
            return "unknown"

        def protos(self):
            if not self.ok: return
            protos = []
            i = 5
            while i < len(self.data):
                if self.data[i] == 0:
                    break
                proto, ending = self.pinfo(i)
                protos.append(proto)
                i += ending
            return protos

        def pinfo(self, pos):
            if not self.ok: return None, 0
            size, length = read_uleb128(self.data[pos:])
            proto = {
                "pos": pos,
                "size": size,
                "size_length": length,
                "fullsize": size + length,
                "flags": self.data[pos + length],
                "params": self.data[pos + length + 1],
                "framesize": self.data[pos + length + 2],
                "numuv": self.data[pos + length + 3]
            }
            pos += length + 4
            proto["numkgc"], proto["numkgc_length"] = read_uleb128(self.data[pos:])
            pos += proto["numkgc_length"]
            proto["numkn"], proto["numkn_length"] = read_uleb128(self.data[pos:])
            pos += proto["numkn_length"]
            proto["numbc"], proto["numbc_length"] = read_uleb128(self.data[pos:])
            proto["numbc_pos"] = pos
            proto["ins"] = pos + proto["numbc_length"]
            return proto, proto["fullsize"]

    if __name__ == "__main__":    
        internet_available = False
        version = os.path.splitext(os.path.basename(sys.argv[0]))[0].split("v")[1].split()[0]
        
        try:
            try:
                
                socket.create_connection(("www.google.com", 80))
                internet_available = True

            except OSError:
                pass

            if internet_available:
                response = get("https://raw.githubusercontent.com/untitled-1111/JitTools/refs/heads/master/check_update")
                response.raise_for_status()
                response_lines = response.text.splitlines()
                new_version = response_lines[0].strip()
                log = "\n".join(response_lines[1:])

                if float(new_version) > float(version):
                    root = tk.Tk()
                    root.withdraw()
                    response = tk.messagebox.askyesno(
                        "Доступно обновление",
                        f"Доступна новая версия JitTools v{new_version}\n\n{log}\n\nОткрыть страницу загрузки?"
                    )
                    if response:
                        import webbrowser
                        webbrowser.open("https://github.com/untitled-1111/JitTools/releases")
        
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            input("[!] В JitTools произошла ошибка, сообщите о ней автору!")
        
        root = tk.Tk()
        root.iconbitmap('icon/icon.ico')
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

        ctypes.windll.user32.SetProcessDPIAware()
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        cx = width // 2
        cy = height // 2
        x = (ctypes.windll.user32.GetSystemMetrics(0) - width) // 2
        y = (ctypes.windll.user32.GetSystemMetrics(1) - height) // 2
        ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, 0)
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # check_file()
        if len(sys.argv) == 2:
            file_path = sys.argv[1]
        else:
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Выберите файл для анализа", filetypes=[("Lua files", "*.lua;*.luac")])
            root.deiconify()
            if not file_path:
                sys.exit()

        root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit()))
        gui(file_path)

except Exception as e:
    print(f"[ERROR] {str(e)}")
    input("[!] В JitTools произошла ошибка, сообщите о ней автору!")
