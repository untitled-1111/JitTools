# Module for JitTools

import os
import tkinter as tk
import sys
import random
import tkinter
import ctypes

def compiler(path):
    try:
        file_path_abs = os.path.abspath(path)
        output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JitTools (C).lua"

        os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
            f' -b "{file_path_abs}"'
            f' "{output_file}"')
        
        tk.messagebox.showinfo("LuaJIT Compiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
    
    except Exception as e:
        tkinter.messagebox.showinfo("JitTools - LuaJIT Compiler", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def joiner(path):
    try:
        file_path = tk.filedialog.askopenfilename(
            title="Выберите файл для склеивания",
            filetypes=[("Lua files", "*.lua;*.luac;*.txt")]
        )
        if not file_path:
            sys.exit()

        with open(path, 'rb') as main_file, open(file_path, 'rb') as file:
            main_data = main_file.read()
            data = file.read()

        roflanEbalo = random.randint(1, random.randint(666, 666666) + random.randint(2, 33)) # даже не спрашивайте

        in_result = f"function jittools_rofl_{random.randint(666, 66666666666)}()\nlocal jittools_rofl_{roflanEbalo} = \"" # не спрашивайте
        in_result += "".join(f"\\x{byte:02X}" for byte in main_data + data)
        in_result += f"\"\nloadstring(jittools_rofl_{roflanEbalo})()\nend\n"

        output_file_name = f"{os.path.splitext(file_path)[0]} - JitTools (SJ){os.path.splitext(file_path)[1]}"
        with open(output_file_name, 'w', encoding='utf-8') as out_file:
            out_file.write(in_result)

        tk.messagebox.showinfo("Joiner", f"Успешно сохранено в файл {os.path.basename(output_file_name)}.")


    except Exception as e:
        tkinter.messagebox.showinfo("JitTools - Joiner", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()