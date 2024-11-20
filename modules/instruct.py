# Module for JitTools

import os
import tkinter as tk

def bcviewer(path):
    file_path_abs = os.path.abspath(path)
    output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JTools (BCL).txt"

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
    output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JTools (ASM).txt"

    result = tk.messagebox.askyesno("ASM", "[!] ASM открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                               "Его необходимо использовать в изолированном пространстве.\n"
                                               "Вы уверены, что хотите открыть ASM? (да/нет)")

    if result:
        os.system(f'python tools\\Decompiler_and_ASM\\main.py'
            f' --catch_asserts --asm --with-line-numbers --file="{file_path_abs}"'
            f' > "{output_file}"')
        
        tk.messagebox.showinfo("ASM", f"Успешно сохранено в файл {os.path.basename(output_file)}.")