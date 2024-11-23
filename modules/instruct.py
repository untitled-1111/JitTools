# Module for JitTools

import os
import tkinter as tk
import sys
import ctypes

def bcviewer(path):
    try:
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
        
    except Exception as e:
        tk.messagebox.showinfo("JitTools - BC Viewer", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def luad():
    try:
        os.system(f'start "" /MAX tools{os.sep}Luad{os.sep}build{os.sep}bin{os.sep}Release{os.sep}luad.exe')

    except Exception as e:
        tk.messagebox.showinfo("JitTools - Luad", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def asm(path):
    try:
        file_path_abs = os.path.abspath(path)
        output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JitTools (ASM).txt"

        result = tk.messagebox.askyesno("ASM", "[!] ASM открывает скрипт на вашем ПК, из-за чего вы будете уязвимы для взлома\n"
                                                "Его необходимо использовать в изолированном пространстве.\n"
                                                "Вы уверены, что хотите открыть ASM? (да/нет)")

        if result:
            os.system(f'python tools\\Decompiler_and_ASM\\main.py'
                f' --catch_asserts --asm --with-line-numbers --file="{file_path_abs}"'
                f' > "{output_file}"')
            
            tk.messagebox.showinfo("ASM", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

    except Exception as e:
        tk.messagebox.showinfo("JitTools - ASM", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()