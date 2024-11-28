# Module for JitTools

import os
import tkinter as tk
import re
import codecs
from ctypes import windll, c_long

windll.kernel32.GetUserDefaultUILanguage.restype = c_long
windll.kernel32.GetUserDefaultUILanguage.argtypes = []
language_id = windll.kernel32.GetUserDefaultUILanguage()

if language_id == 1049:
    lang = {
        "saved": "Успешно сохранено в файл",
    }
else:
    lang = {
        "saved": "Successfully saved to file",
    }

def base64d(arg):
    os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
            f' tools{os.sep}Debugger{os.sep}Base64_Roflan.lua -d "{arg}"')
  
def shitd(file_path):
    output = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}\\{os.path.splitext(os.path.basename(file_path))[0]}"

    base_filename = os.path.basename(file_path)
    match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.(?:lua|luac)$', base_filename)
    if match:
        output_file_name = f"{match.group('base')} - JitTools ({match.group('type')} + SD).lua"
    else:
        output_file_name = f"{output} - JitTools (SD).lua"
    
    table_re = re.compile(r"(\{[\n\r\t \d,]*?\})")
    number_re = re.compile(r"\d+")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = file.read()
    entries = []
    for match in table_re.finditer(data):
        group = match.group(0)
        table = group.replace("\r", "").replace("\n", "").replace("\t", "")

        if table == "{}" or table == "{1}":
            continue

        bytes_list = [int(num) for num in number_re.findall(table)]
        entries.append(EncodedEntry(bytes_list, match.start(), match.end()))

    offset = 0
    with open(output_file_name, 'w', encoding='utf-8', errors='ignore') as out_file:
        for entry in entries:
            out_file.write(data[offset:entry.start])
            val = entry.decode()
            if val is not None:
                out_file.write(f"[[{val}]]")
            else:
                out_file.write(data[entry.start:entry.end])
            offset = entry.end
        out_file.write(data[offset:])

    tk.messagebox.showinfo("Shit Deobfuscation", f"{lang['saved']}: {os.path.basename(output_file_name)}.")
  
class EncodedEntry:
  def __init__(self, bytes, start, end):
      self.bytes = bytes
      self.start = start
      self.end = end

  def decode(self):
      if self.bytes[0] != len(self.bytes):
          return None
      bytes_decoded = [
          (0xff - ((byte - index - 1) & 0xff)) & 0xff
          for index, byte in enumerate(self.bytes[1:])
      ]
      try:
          return codecs.decode(bytes(bytes_decoded), 'windows-1251')
      except Exception:
          return None

  def decode2(self):
      if len(self.bytes) < 11:
          return None
      bytes_decoded = [
          (0xff - (byte & 0xff)) & 0xff
          for index, (byte, a) in enumerate(zip(self.bytes[11:], range(11 + self.bytes[10] - self.bytes[0])))
      ]
      try:
          return codecs.decode(bytes(bytes_decoded), 'windows-1251')
      except Exception:
          return None