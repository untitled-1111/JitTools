# Module for JitTools

import os
import time
import tkinter as tk
import re
from ctypes import windll, c_long

windll.kernel32.GetUserDefaultUILanguage.restype = c_long
windll.kernel32.GetUserDefaultUILanguage.argtypes = []
language_id = windll.kernel32.GetUserDefaultUILanguage()

if language_id == 1049:
    lang = {
        "error_compiled": "не является скомпилированным LuaJIT скриптом",
        "warning_1": "открывает скрипт на вашем компьютере, делая вас уязвимым к взлому",
        "warning_2": "Он должен быть использован в изолированном пространстве",
        "warning_3": "Вы уверены, что хотите открыть",
        "warning_4": "(да/нет)",
        "saved": "Успешно сохранено в файл",
    }
else:
    lang = {
        "error_compiled": "is not a compiled LuaJIT script",
        "warning_1": "opens a script on your computer, leaving you vulnerable to hacking",
        "warning_2": "It must be used in an isolated space",
        "warning_3": "Are you sure you want to open",
        "warning_4": "(yes/no)",
        "saved": "Successfully saved to file",
    }

def editor(path):
    os.chdir(f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}tools{os.sep}Bytecode_Editor")
    os.system(f'start "" /MAX Bytecode_Fucker.exe "{path}"')

    process_name = "Bytecode_Fucker.exe"
    while True:
        process_list = os.popen('tasklist').read().strip().lower()
        if process_name.lower() not in process_list:
            os.chdir(f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}")
            break

        time.sleep(1)

def bcviewer(path):
    file_path_abs = os.path.abspath(path)
    output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}{os.path.splitext(os.path.basename(path))[0]} - JitTools (BCL).txt"

    with open(path, 'rb') as f:
        data = f.read(3)
    if data != b'\x1B\x4C\x4A': # magic bytes
        tk.messagebox.showerror("BC Viewer", f"{os.path.basename(path)} {lang['error_compiled']}.")
    else:
        os.system(f'tools{os.sep}BCLister.exe'
            f' "{file_path_abs}"'
            f' "{output_file}"')
        
        tk.messagebox.showinfo("BC Viewer", f"{lang['saved']}: {os.path.basename(output_file)}.")

def luad(file_path, main_ext):
    os.system(f'start "" /MAX tools{os.sep}Luad{os.sep}build{os.sep}bin{os.sep}Release{os.sep}luad.exe')

    process_name = "luad.exe"
    while True:
        process_list = os.popen('tasklist').read().strip().lower()
        if process_name.lower() not in process_list:
            base = os.path.splitext(os.path.basename(file_path))[0]
            new_file_path = base + main_ext
            
            os.rename(base + ".luac", new_file_path)
            break

        time.sleep(1)

def asm(path):
    file_path_abs = os.path.abspath(path)
    output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{os.sep}{os.path.splitext(os.path.basename(path))[0]}"

    base_filename = os.path.basename(path)
    match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.(?:lua|luac)$', base_filename)
    if match:
        output_file = f"{match.group('base')} - JitTools ({match.group('type')} + ASM).txt"
    else:
        output_file = f"{output} - JitTools (ASM).txt"

    result = tk.messagebox.askyesno("ASM", f"[!] ASM {lang['warning_1']}\n"
                                            f"{lang['warning_2']}.\n"
                                            f"{lang['warning_3']} ASM? {lang['warning_4']}")

    if result:
        os.system(f'python tools{os.sep}Decompiler_and_ASM{os.sep}main.py'
            f' --catch_asserts --asm --with-line-numbers --file="{file_path_abs}"'
            f' > "{output_file}"')

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            tk.messagebox.showinfo("ASM", f"{lang['saved']}: {os.path.basename(output_file)}.")
        else:
          os.remove(output_file)
          
          result = tk.messagebox.showerror("ASM", lang['error_console'])
          if result:
            hwnd = windll.kernel32.GetConsoleWindow()
            windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL
