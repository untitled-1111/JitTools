# Module for JitTools

import os
import tkinter as tk
import sys
import random

def compiler(path):
  file_path_abs = os.path.abspath(path)
  output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JTools (LJ_C).lua"

  os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
      f' -b "{file_path_abs}"'
      f' "{output_file}"')
  
  tk.messagebox.showinfo("LuaJIT Compiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

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

        roflanEbalo = random.randint(1, random.randint(666, 66666666666)) # даже не спрашивайте

        in_result = f"jittools_rofl_{roflanEbalo} = \""
        in_result += "".join(f"\\x{byte:02X}" for byte in main_data + data)
        in_result += f"\"\nloadstring(jittools_rofl_{roflanEbalo})()\n\n"

        output_file_name = f"{os.path.splitext(file_path)[0]} - JTools (SJ){os.path.splitext(file_path)[1]}"
        with open(output_file_name, 'w', encoding='utf-8') as out_file:
            out_file.write(in_result)

        tk.messagebox.showinfo("Joiner", f"Успешно сохранено в файл {os.path.basename(output_file_name)}.")
    except Exception as e:
        print(f"[Joiner] {str(e)}")
        input("[!] В JitTools произошла ошибка, сообщите о ней автору!")
