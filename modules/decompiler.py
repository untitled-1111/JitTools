# Module for JitTools

import os
import tkinter as tk
import sys
import ctypes

def ljd_decompiler(path):
  try:
    with open(path, 'rb') as f:
      data = f.read(3)
      if data != b'\x1B\x4C\x4A': # magic bytes
        tk.messagebox.showerror("LJD Decompiler", f"{os.path.basename(path)} не является скомпилированным LuaJIT скриптом.")
      else:
        file_path_abs = os.path.abspath(path)
        output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JitTools (LD).lua"
        
        os.system(f'python "tools{os.sep}LJD_Decompiler{os.sep}main.py"'
            f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
            f' --output="{output_file}"')

        if os.path.exists(output_file):
            tk.messagebox.showinfo("LJD Decompiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

  except Exception as e:
        tk.messagebox.showinfo("JitTools - LJD Decompiler", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()

def py_decompiler(path):
  try:
    with open(path, 'rb') as f:
      data = f.read(3)
      if data != b'\x1B\x4C\x4A': # magic bytes
        tk.messagebox.showerror("Py Decompiler", f"{os.path.basename(path)} не является скомпилированным LuaJIT скриптом.")
      else:
        file_path_abs = os.path.abspath(path)
        output_file = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]} - JitTools (PD).lua"
        
        os.system(f'python "tools{os.sep}Decompiler_and_ASM{os.sep}main.py"'
            f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
            f' --output="{output_file}"')

        if os.path.exists(output_file):
            tk.messagebox.showinfo("Py Decompiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")

  except Exception as e:
        tk.messagebox.showinfo("JitTools - Python Decompiler", f"Произошла ошибка:\n[{e.__traceback__.tb_lineno}]: {e}")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1) # SW_NORMAL
        sys.exit()