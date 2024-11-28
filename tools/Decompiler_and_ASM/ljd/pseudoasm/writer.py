#
# Copyright (C) 2013 Andrian Nord. See Copyright Notice in main.py
#

import ljd.pseudoasm.prototype
import ljd.util.indentedstream
from ljd.bytecode.constants import T_NIL, T_FALSE, T_TRUE

OPCODES = set(range(0x00, 0x3a))

class _State:
    def __init__(self):
        self.flags = None
        self.stream = None
        self.source = None

def write(fd, header, prototype):
    writer = _State()

    writer.stream = ljd.util.indentedstream.IndentedStream(fd)
    writer.flags = header.flags
    writer.source = "N/A" if header.flags.is_stripped else header.name

    _write_header(writer, header)

    ljd.pseudoasm.prototype.write(writer, prototype)


def _write_header(writer, header):
    writer.stream.write_multiline("""
;
; Flags:
;	Endianness: {endianness}
;	FFI: {ffi}
;

""", origin=header.origin,
                                  endianness="Big" if header.flags.is_big_endian else "Little",
                                  ffi="Present" if header.flags.has_ffi else "Not present")

