# Module for JitTools

import os
import tkinter as tk
import sys
import re
import subprocess

def compiler(path):
    file_path_abs = os.path.abspath(path)
    output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]}"

    base_filename = os.path.basename(path)
    match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.(?:lua|luac)$', base_filename)
    if match:
        output_file = f"{match.group('base')} - JitTools ({match.group('type')} + C).lua"
    else:
        output_file = f"{output} - JitTools (C).lua"

    process = subprocess.Popen(
        [f'tools{os.sep}Debugger{os.sep}luajit.exe', '-b', file_path_abs, output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    stdout, stderr = process.communicate()

    if stderr:
        match = re.search(r'(?P<file>.*)\:(?P<line>\d+)\:(?P<msg>.*)', stderr)
        if match:
            tk.messagebox.showerror("LuaJIT Compiler", f"Прозиошла ошибка: \n[{match.group('line')}]{match.group('msg')}")
        else:
            tk.messagebox.showinfo("LuaJIT Compiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
    else:
        tk.messagebox.showinfo("LuaJIT Compiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

def joiner(path):
    file_path = tk.filedialog.askopenfilename(
        title=f"Выберите файл для склеивания [{os.path.basename(path)}]",
        filetypes=[("Lua files", "*.lua;*.luac;*.txt")]
    )
    if not file_path:
        sys.exit()

    with open(path, 'rb') as main_file, open(file_path, 'rb') as file:
        main_data = main_file.read()
        data = file.read()

    in_result = f'loadstring("'
    in_result += "".join(f"\\x{byte:02X}" for byte in main_data + data)
    in_result += '")()'

    output_file_name = f"{os.path.splitext(file_path)[0]} - JitTools (SJ){os.path.splitext(file_path)[1]}"
    with open(output_file_name, 'w', encoding='utf-8') as out_file:
        out_file.write(in_result)

    tk.messagebox.showinfo("Joiner", f"Успешно сохранено в файл {os.path.basename(output_file_name)}.")