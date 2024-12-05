# Module for JitTools

import os
import sys
import pathlib
import re

import tkinter as tk
from ctypes import windll, c_long

windll.kernel32.GetUserDefaultUILanguage.restype = c_long
windll.kernel32.GetUserDefaultUILanguage.argtypes = []
language_id = windll.kernel32.GetUserDefaultUILanguage()

if language_id == 1049:
    lang = {
        "error_compiled": "не является скомпилированным LuaJIT скриптом",
        "saved": "Успешно сохранено в файл",
        "err_unprot": "Необходимых инструкций не найдено.",
    }
else:
    lang = {
        "error_compiled": "is not a compiled LuaJIT script",
        "saved": "Successfully saved to file",
        "err_unprot": "No instructions found.",
    }

def unprot_2(path):
  with open(path, 'rb') as f:
    data = f.read(3)
    if data != b'\x1B\x4C\x4A': # magic bytes
      tk.messagebox.showerror("Unprot v2.1", f"{os.path.basename(path)} {lang['error_compiled']}.")
    else:
        script = LuaJIT(path)
        protos = script.get_protos()
        proto_num = 0

        for proto in reversed(protos):
            proto_start = proto["ins"]
            proto_end = proto_start + proto["numbc"] * 4 
            proto_data = script.data[proto_start : proto_end]
            jump_off, trash_opcodes, jump_max = 0, 0, 0
            
            while True:
                opcode = proto_data[jump_off]
                if opcode == 0x12:
                    jump_off += 4
                    trash_opcodes += 1
                    continue
                if opcode == 0x58 or opcode == 0x32:
                    jmp_dist = read_uint16(proto_data[jump_off + 2 : jump_off + 4]) + 1
                    trash_opcodes += jmp_dist
                    jump_off += 4 * jmp_dist
                    continue
                break
            while True:
                opcode, jmp_down, uint = opcode_info(proto_data, jump_off)
                if opcode == 0x32 or (opcode == 0x58 and jmp_down):
                    tmp = new_dist(jump_off, uint)
                    if len(proto_data) > tmp > jump_max: jump_max = tmp
                    jump_off += 4
                    continue
                if opcode in ret_opcodes:
                    if jump_off < jump_max:
                        jump_off += 4
                        continue
                    script.data[proto_start + jump_off + 4 : proto_end] = []
                    script.data[proto_start : proto_start + trash_opcodes * 4] = []
                    total_opcodes = proto["numbc"] - (jump_off // 4 - trash_opcodes) - 1
                    
                    # updating number of opcodes
                    numbc_pos = proto["numbc_pos"]
                    length = proto["numbc_length"]     
                    script.data[numbc_pos : numbc_pos + length], new_length = write_uleb128(proto["numbc"] - total_opcodes)
                    
                    extra_length = 0
                    if new_length < length:
                        extra_length = new_length - length
                    
                    # updating prototype size
                    proto_pos = proto["pos"]
                    proto_size, length = read_uleb128(script.data[proto_pos:])
                    script.data[proto_pos : proto_pos + length], _ = write_uleb128(proto_size - (total_opcodes * 4) + extra_length)
                    break            
                jump_off += 4
                continue   
            proto_num += 1

        new_size = len(script.data)
        old_size = os.path.getsize(path)
        if new_size != old_size:
            base_filename = os.path.basename(path)

            match = re.search(r'(?P<base>.*) - JitTools \((?P<type>.*)\)\.lua$', base_filename)
            if match:
                output_file = f"{match.group('base')} - JitTools ({match.group('type')} + U).lua"
            else:
                output_file = f"{os.path.splitext(base_filename)[0]} - JitTools (U).lua"

            pathlib.Path(output_file).write_bytes(script.data)
            tk.messagebox.showinfo("Unprot v2.1", f"{lang['saved']}: {os.path.basename(output_file)}.")
        else:
            tk.messagebox.showinfo("Unprot v2.1", f"{lang['err_unprot']}")
    
ret_opcodes = [0x49, 0x4A, 0x4B, 0x4C, 0x43, 0x44]

def opcode_info(data, pos):
    return data[pos], data[pos + 3] >= 128, read_uint16(data[pos + 2 : pos + 4])

def new_dist(offset, dist):
    opcode_pos = offset // 4
    return (opcode_pos + dist + 1) * 4

class LuaJIT:
    def __init__(self, path):
        self.path = path
        self.data = bytearray(pathlib.Path(path).read_bytes()) if os.path.exists(path) else None
        self.ok = self.data != None and len(self.data) > 5 and self.data[:3] == b"\x1B\x4C\x4A"

    def exists(self):
        return os.path.exists(self.path)

    def isCompiled(self):
        return self.ok

    def version(self):
        if self.ok:
            return self.data[3]

    def get_proto(self, proto_id):
        return self.get_protos()[proto_id]

    def get_protos(self):
        if not self.ok: return
        protos = []
        i = 5
        while i < len(self.data):
            if self.data[i] == 0:
                break
            proto, ending = self.pinfo(i)
            protos.append(proto)
            i += ending
        return protos

    def pinfo(self, pos):
        if not self.ok: return None, 0
        size, length = read_uleb128(self.data[pos:])
        proto = {
            "pos": pos,
            "size": size,
            "size_length": length,
            "fullsize": size + length,
            "flags": self.data[pos + length],
            "params": self.data[pos + length + 1],
            "framesize": self.data[pos + length + 2],
            "numuv": self.data[pos + length + 3]
        }
        pos += length + 4
        proto["numkgc"], proto["numkgc_length"] = read_uleb128(self.data[pos:])
        pos += proto["numkgc_length"]
        proto["numkn"], proto["numkn_length"] = read_uleb128(self.data[pos:])
        pos += proto["numkn_length"]
        proto["numbc"], proto["numbc_length"] = read_uleb128(self.data[pos:])
        proto["numbc_pos"] = pos
        proto["ins"] = pos + proto["numbc_length"]
        return proto, proto["fullsize"]

def read_uleb128(data):
    value = 0
    for i in range(len(data)):
        tmp = data[i] & 0x7f
        value = tmp << (i * 7) | value
        if (data[i] & 0x80) != 0x80:
            break
    return value, i + 1

def write_uleb128(integer):
    result = bytearray(b'')
    while True:
        byte = integer & 0x7f
        integer >>= 7
        if integer != 0: byte |= 0x80
        result.append(byte)
        if integer == 0: break
    return result, len(result)

def read_sleb128(value):
    result = 0
    shift = 0
    while True:
        byte = value.shift()
        result |= (byte & 0x7f) << shift
        shift += 7
        if ((0x80 & byte) == 0):
            if shift < 32 and (byte & 0x40) != 0:
                return result | (~0 << shift)
            return result

def write_sleb128(integer):
    integer |= 0
    result = bytearray(b'')
    while True:
        byte = integer & 0x7f
        integer >>= 7
        if (integer != 0 and (byte & 0x40)) or (integer == -1 and (byte & 0x40) != 0):
            result.append(byte)
            return result, len(result)
        result.append(byte | 0x80)
    return result, len(result)

def write_uint16(integer):
    result = bytearray(b'\x00\x80')
    while True:
        byte = integer - 0x100
        if byte >= 0:
            result[1] += 1
            integer -= 0x100
        else:
            result[0] += integer
            break
    return result

def read_uint16(bytecode):
    hexbc = bytecode.hex()
    integer = bytecode[0]
    byte = bytecode[1] - 0x80
    if byte > 0:
        integer = int(format(byte, 'x') + hexbc[0 : 2], 16)
    return integer

def file_read(path):
    if os.path.exists(path):
        return True, bytearray(pathlib.Path(path).read_bytes())
    return False, None

def parse_files():
    files = []
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            if os.path.isfile(i) and os.path.exists(i): files.append(i)
            else: tk.messagebox.showinfo("Error", "File cannot be found: " + i)
    if not len(files):
        tk.messagebox.showinfo("Error", "No file has been chosen")
        sys.exit()
    return files

def prompt(Text, Type = ""):
    if Type.lower() == "int" or Type.lower() == "integer":
        return int(input(Text))
    if Type.lower() == "path":
        return input(Text).replace("\"", "")
    return input(Text)