# Module for JitTools

import os
import tkinter as tk
import re
from ctypes import windll

def ljd_decompiler(path):
  with open(path, 'rb') as f:
    data = f.read(3)
    if data != b'\x1B\x4C\x4A': # magic bytes
      tk.messagebox.showerror("LJD Decompiler", f"{os.path.basename(path)} не является скомпилированным LuaJIT скриптом.")
    else:
      file_path_abs = os.path.abspath(path)
      output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]}"

      base_filename = os.path.basename(path)
      match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.lua$', base_filename)
      if match:
          output_file = f"{match.group('base')} - JitTools ({match.group('type')} + LD).lua"
      else:
          output_file = f"{output} - JitTools (LD).lua"
      
      os.system(f'python "tools{os.sep}LJD_Decompiler{os.sep}main.py"'
            f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
            f' --output="{output_file}"')

      if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
          tk.messagebox.showinfo("LJD Decompiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
      else:
          os.remove(output_file)

          result = tk.messagebox.showerror("LJD Decompiler", "Прозошла ошибка при декомпиляции, подробную информацию можно посмотреть в консоли.")
          if result:
            hwnd = windll.kernel32.GetConsoleWindow()
            windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL

def py_decompiler(path):
  with open(path, 'rb') as f:
    data = f.read(3)
    if data != b'\x1B\x4C\x4A': # magic bytes
      tk.messagebox.showerror("Py Decompiler", f"{os.path.basename(path)} не является скомпилированным LuaJIT скриптом.")
    else:
      file_path_abs = os.path.abspath(path)
      output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(path))[0]}"

      base_filename = os.path.basename(path)
      match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.(?:lua|luac)$', base_filename)
      if match:
          output_file = f"{match.group('base')} - JitTools ({match.group('type')} + PD).lua"
      else:
          output_file = f"{output} - JitTools (PD).lua"

      os.system(f'python "tools{os.sep}Decompiler_and_ASM{os.sep}main.py"'
          f' --catch_asserts --with-line-numbers --file="{file_path_abs}"'
          f' --output="{output_file}"')

      if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
          tk.messagebox.showinfo("LJD Decompiler", f"Успешно сохранено в файл {os.path.basename(output_file)}.")
      else:
          os.remove(output_file)
          
          result = tk.messagebox.showerror("LJD Decompiler", "Прозошла ошибка при декомпиляции, подробную информацию можно посмотреть в консоли.")
          if result:
            hwnd = windll.kernel32.GetConsoleWindow()
            windll.user32.ShowWindow(hwnd, 1) # SW_NORMAL