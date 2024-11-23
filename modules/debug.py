# Module for JitTools

import os
import tkinter as tk
import sys
import ctypes

def moonsecdump(path):
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
          local string = '[FUNCTION CALL] Функция: ' .. name .. ' Код: ' .. info.source
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
                  local string = '[FUNCTION DUMPER] Создана функция: ' .. tostring(key)
                  debugInfo('functions - JitTools (Moonsec).txt', string) 
                  rawset(t, key, wrapFunction(value, tostring(key)))  
              elseif type(value) == 'table' then
                  local string = '[TABLE DUMPER] Создана таблица: ' .. tostring(key)
                  debugInfo('tables - JitTools (Moonsec).txt', string)  
                  rawset(t, key, value) 
              else
                  local string = '[VARIABLE SET] Переменная: ' .. tostring(key) .. ' = ' .. tostring(value)
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

    print('[MOONSEC-DUMPER] HOOKS INSTALLED =)')  
  end

  MoonSecHook();"""
        with open(path, 'r+b') as file:
            content = file.read()
            try:
                file_content = content.decode('utf-8')
            except UnicodeDecodeError:
                file_content = content.decode('cp1251')
            file.seek(0)
            file.write((private_roflan + file_content).encode('utf-8'))

        file_path_abs = os.path.abspath(path)
        os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
            f' "{file_path_abs}"')

        tk.messagebox.showinfo("Dumper", f"Дампы успешно сохранены в папку: {os.path.dirname(path)}")

  except Exception as e:
      tk.messagebox.showinfo("JitTools - Moonsec Dumper", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
      ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
      sys.exit()

def hookobf(path):
    try:
      result = tk.messagebox.askyesno("Hook Obf", "[!] Hook Obf открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                              "Его необходимо использовать в изолированном пространстве.\n"
                                              "Вы уверены, что хотите открыть Hook Obf? (да/нет)")
      
      if result:
        file_path_abs = os.path.abspath(path)
        os.system(f'tools{os.sep}Hook_Obfuscation{os.sep}luajit.exe'
            f' tools{os.sep}Hook_Obfuscation{os.sep}main.lua "{file_path_abs}"')
        
    except Exception as e:
        tk.messagebox.showinfo("JitTools - Hook Obf", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def debugger(path):
    try:
      result = tk.messagebox.askyesno("Debugger", "[!] Debugger открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                              "Его необходимо использовать в изолированном пространстве.\n"
                                              "Вы уверены, что хотите открыть Debugger? (да/нет)")
      
      if result:
        file_path_abs = os.path.abspath(path)
        os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
            f' tools{os.sep}Debugger{os.sep}!0LuaRuntimeChecker.lua "{file_path_abs}"')

        tk.messagebox.showinfo("Debugger", f"Дампы функций могут находиться в этой папке: {os.path.join(os.path.dirname(file_path_abs), 'dumps')}")
    
    except Exception as e:
        tk.messagebox.showinfo("JitTools - Debugger", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def xorunpack(path):
    try:
      result = tk.messagebox.askyesno("XOR Unpack", "[!] XOR Unpack открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                              "Его необходимо использовать в изолированном пространстве.\n"
                                              "Вы уверены, что хотите открыть XOR Unpack? (да/нет)")
      
      if result:
        file_path_abs = os.path.abspath(path)
        os.system(f'tools{os.sep}XOR_Unpacker{os.sep}CLI.exe'
            f' "{file_path_abs}"')
        
    except Exception as e:
        tk.messagebox.showinfo("JitTools - XOR Unpack", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()