# Module for JitTools

import os
import tkinter as tk
import re
from ctypes import windll

def bcviewer(path):
    file_path_abs = os.path.abspath(path)
    output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JitTools (BCL).txt"

    with open(path, 'rb') as f:
        data = f.read(3)
    if data != b'\x1B\x4C\x4A': # magic bytes
        tk.messagebox.showerror("BC Viewer", f"{os.path.basename(path)} не является скомпилированным LuaJIT скриптом.")
    else:
        os.system(f'tools{os.sep}BCLister.exe'
            f' "{file_path_abs}"'
            f' "{output_file}"')
        
        tk.messagebox.showinfo("BC Viewer", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

def luad():
    os.system(f'start "" /MAX tools{os.sep}Luad{os.sep}build{os.sep}bin{os.sep}Release{os.sep}luad.exe')

def asm(path):
    file_path_abs = os.path.abspath(path)
    output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]}"

    base_filename = os.path.basename(path)
    match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.(?:lua|luac)$', base_filename)
    if match:
        output_file = f"{match.group('base')} - JitTools ({match.group('type')} + ASM).txt"
    else:
        output_file = f"{output} - JitTools (ASM).txt"

    result = tk.messagebox.askyesno("ASM", "[!] ASM открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                            "Его необходимо использовать в изолированном пространстве.\n"
                                            "Вы уверены, что хотите открыть ASM? (да/нет)")

    if result:
        os.system(f'python tools\\Decompiler_and_ASM\\main.py'
            f' --catch_asserts --asm --with-line-numbers --file="{file_path_abs}"'
            f' > "{output_file}"')

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            tk.messagebox.showinfo("ASM", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
        else:
          os.remove(output_file)
          
          result = tk.messagebox.showerror("ASM", "Прозошла ошибка при декомпиляции, подробную информацию можно посмотреть в консоли.")
          if result:
            hwnd = windll.kernel32.GetConsoleWindow()
            windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL