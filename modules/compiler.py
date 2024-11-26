# Module for JitTools

import os
import tkinter as tk
import sys
import re
import subprocess
import pathlib

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
        title=f"Выберите второй файл для склеивания [{os.path.basename(path)}]",
        filetypes=[("Lua files", "*.lua;*.luac;*.txt")]
    )
    if not file_path:
        sys.exit()

    for i in range(0, 1):
        data = bytearray(pathlib.Path(path).read_bytes())
        data_two = bytearray(pathlib.Path(file_path).read_bytes())

        result = "loadstring(\""
        for j in data:
            result += f"\\x{j:02X}"
        result += "\")()\n"

        result += "loadstring(\""
        for j in data_two:
            result += f"\\x{j:02X}"
        result += "\")()"
        
        output_file_name = f"{os.path.splitext(file_path)[0]} - JitTools (J){os.path.splitext(file_path)[1]}"
        pathlib.Path(output_file_name).write_text(result)

    tk.messagebox.showinfo("Joiner", f"Успешно сохранено в файл {os.path.basename(output_file_name)}.")