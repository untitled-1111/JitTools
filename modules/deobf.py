# Module for JitTools

import os
import tkinter as tk
import re
import codecs

def base64d(arg):
  os.system(f'tools{os.sep}Debugger{os.sep}luajit.exe'
        f' tools{os.sep}Debugger{os.sep}Base64_Roflan.lua -d "{arg}"')
  
def shitd(file_path):
  input_file_name, input_file_extension = os.path.splitext(file_path)
  output_file_name = f"{input_file_name} - JTools (SD){input_file_extension}"
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

  tk.messagebox.showinfo("Shit Deobfuscation", f"Успешно сохранено в файл {os.path.basename(output_file_name)}.")
  
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