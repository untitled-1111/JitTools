# Module for JitTools

import os
import tkinter as tk
import subprocess
import re
from ctypes import windll, c_long

windll.kernel32.GetUserDefaultUILanguage.restype = c_long
windll.kernel32.GetUserDefaultUILanguage.argtypes = []
language_id = windll.kernel32.GetUserDefaultUILanguage()

if language_id == 1049:
    lang = {
        "error_desc": "Произошла ошибка",
        "warning_1": "открывает скрипт на вашем компьютере, делая вас уязвимым к взлому",
        "warning_2": "Он должен быть использован в изолированном пространстве",
        "warning_3": "Вы уверены, что хотите открыть",
        "warning_4": "(да/нет)",
        "dumps_saved": "Дампы успешно сохранены в папке",
        "dumps_warning": "Количество файлов превышает 3, удалить все, кроме самого большого?",
        "error_compiled": "Данный файл скомпилирован, дальнейшая работа невозможна.",
        "error_no_dumps": "Дампы не были созданы.",
    }
else:
    lang = {
        "error_desc": "An error has occurred",
        "warning_1": "opens a script on your computer, leaving you vulnerable to hacking",
        "warning_2": "It must be used in an isolated space",
        "warning_3": "Are you sure you want to open",
        "warning_4": "(yes/no)",
        "dumps_saved": "Dumps successfully saved in folder",
        "dumps_warning": "The number of files exceeds 3, delete all except the largest?",
        "error_compiled": "This file is compiled, further work is impossible.",
        "error_no_dumps": "Dumps were not created.",
    }

def moonsecdump(path):
  result = tk.messagebox.askyesno("Moonsec Dumper", f"[!] Dumper {lang["warning_1"]}\n"
                                            f"{lang['warning_2']}.\n"
                                            f"{lang['warning_3']} Dumper? {lang['warning_4']}")
            
  if result:
      private_roflan = """local function MoonSecHook()
    local anti_tamper = string.match
    local unpack_orig = table.unpack

    string.match = function(a,b) -- // moonsec anti-tamper
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
          debugInfo('require - JitTools (Moonsec).txt', v)
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
          local string = '[FUNCTION CALL] Function: ' .. name .. ' Code: ' .. info.source
          debugInfo('function_call - JitTools (Moonsec).txt', string) 
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
                local string = '[FUNCTION DUMPER] Created function: ' .. tostring(key)
                debugInfo('functions - JitTools (Moonsec).txt', string) 
                rawset(t, key, wrapFunction(value, tostring(key)))  
            elseif type(value) == 'table' then
                local string = '[TABLE DUMPER] Created table: ' .. tostring(key)
                debugInfo('tables - JitTools (Moonsec).txt', string)  
                rawset(t, key, value) 
            else
                local string = '[VARIABLE SET] Variable: ' .. tostring(key) .. ' = ' .. tostring(value)
                debugInfo('variables - JitTools (Moonsec).txt', string)  
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
            debugInfo('dump - JitTools (Moonsec).txt', table_to_string(v) .. '\\n')
          else
            debugInfo('dump - JitTools (Moonsec).txt', string.format('{Key: %s | Val: %s}\\n', tostring(k), tostring(v)))
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
end

MoonSecHook();"""
      base_filename = os.path.splitext(os.path.basename(path))[0]
      output_file_name = f"{base_filename} - JitTools (M){os.path.splitext(os.path.basename(path))[1]}"
      
      with open(path, 'rb') as file:
          data = file.read(3) # читаем 3 байта
          if data == b'\x1B\x4C\x4A': # если они равны magic байтам (compiled LuaJIT)
              tk.messagebox.showerror("Dumper", f"{lang['error_compiled']}")
          else:
            with open(output_file_name, 'wb') as out_file:
                file.seek(0) # возвращаемся к 0 байту (началу файла)
                content = file.read()
                file_content = content.decode('cp1251')
                out_file.write((private_roflan + file_content).encode('cp1251'))

                file_path_abs = os.path.abspath(output_file_name)
                process = subprocess.Popen(
                  [f'tools{os.sep}Debugger{os.sep}luajit.exe', file_path_abs],
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  universal_newlines=True
                )

                stdout, stderr = process.communicate()

                if stderr:
                    match = re.search(r'(?P<file>.*)\:(?P<line>\d+)\:(?P<msg>.*)', stderr)
                    if match:
                        tk.messagebox.showerror("Dumper", f"{lang['error_desc']}: \n[{match.group('line')}]{match.group('msg')}")
                    else:
                        tk.messagebox.showinfo("Dumper", f"{lang["dumps_saved"]}: {os.path.dirname(path)}")
                else:
                  tk.messagebox.showinfo("Dumper", f"{lang["dumps_saved"]}: {os.path.dirname(path)}.")

def hookobf(path):
    result = tk.messagebox.askyesno("Hook Obf", f"[!] Hook Obf {lang['warning_1']}\n"
                                            f"{lang['warning_2']}.\n"
                                            f"{lang['warning_3']} Hook Obf? {lang['warning_4']}")
    
    if result:
      file_path_abs = os.path.abspath(path)
      os.system(f'tools{os.sep}Hook_Obfuscation{os.sep}luajit.exe'
          f' tools{os.sep}Hook_Obfuscation{os.sep}main.lua "{file_path_abs}"')
      
      directory = os.path.dirname(file_path_abs)
      pattern = re.compile(r'^.*\[\d+\]\.lua$')
      lua_files = [f for f in os.listdir(directory) if pattern.match(f)]
      file_sizes = [os.path.getsize(os.path.join(directory, f)) for f in lua_files]

      if len(lua_files) > 3:
          result = tk.messagebox.askyesno("Hook Obf", f"{lang['dumps_warning']}")
          if result:
            largest_file = lua_files[file_sizes.index(max(file_sizes))]
            save_path = os.path.join(directory, f"{os.path.splitext(os.path.basename(largest_file))[0]} - JitTools (H).lua")
            with open(os.path.join(directory, largest_file), "rb") as src_file, open(save_path, "wb") as dst_file:
                    dst_file.write(src_file.read())

            for filename in lua_files:
                file_to_remove = os.path.join(directory, filename)
                os.remove(file_to_remove)

      if not lua_files:
          tk.messagebox.showerror("Hook Obf", f"{lang['error_no_dumps']}")
      else:
        tk.messagebox.showinfo("Hook Obf", f"{lang["dumps_saved"]}: {os.path.join(os.path.dirname(file_path_abs))}")

def debugger(path):
    result = tk.messagebox.askyesno("Debugger", f"[!] Debugger {lang['warning_1']}\n"
                                            f"{lang['warning_2']}.\n"
                                            f"{lang['warning_3']} Debugger? {lang['warning_4']}")
    
    if result:
      file_path_abs = os.path.abspath(path)

      os.chdir(f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}tools{os.sep}Debugger")
      os.system(f'luajit.exe'
          f' !0LuaRuntimeChecker.lua "{file_path_abs}"')

      dumps_dir = os.path.join(f'{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}tools{os.sep}Debugger', 'dumps')
      files = [f for f in os.listdir(dumps_dir) if not f.endswith('.ini')]
      if files:
          for file in files:
              file_src = os.path.join(dumps_dir, file)
              file_dst = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(dumps_dir))), 'dumps', file)
              with open(file_src, 'rb') as src_file, open(file_dst, 'wb') as dst_file:
                  dst_file.write(src_file.read())
              os.remove(file_src)

              tk.messagebox.showinfo("Debugger", f"{lang["dumps_saved"]}: {os.path.join(os.path.dirname(file_path_abs), 'dumps')}")
      else:
          tk.messagebox.showerror("Debugger", f"{lang['error_no_dumps']}")

      os.chdir(f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}")

def xorunpack(path):
    result = tk.messagebox.askyesno("XOR Unpack", f"[!] XOR Unpack {lang['warning_1']}\n"
                                            f"{lang['warning_2']}.\n"
                                            f"{lang['warning_3']} XOR Unpack? {lang['warning_4']}")
    
    if result:
      file_path_abs = os.path.abspath(path)
      os.system(f'tools{os.sep}XOR_Unpacker{os.sep}CLI.exe'
          f' "{file_path_abs}"')