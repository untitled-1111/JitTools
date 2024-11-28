#!/usr/bin/env python3

from argparse import ArgumentParser
import main as ljdcore

import ljd.rawdump.parser
import ljd.ast.printast
import ljd.ast.builder
import ljd.ast.validator

import bcdiff.astwalker


def main():
    parser = ArgumentParser()

    parser.add_argument('files', type=str, nargs=2, metavar='file',
                        help="Bytecode files to be compared")

    args = parser.parse_args()

    ast_a = _build_ast(args.files[0])
    ast_b = _build_ast(args.files[1])

    bcdiff.astwalker.compare_ast(ast_a, ast_b)


def _build_ast(filename):
    def on_parse_header(preheader):
        # Identify the version of LuaJIT used to compile the file
        bc_version = None
        if preheader.version == 1:
            bc_version = 2.0
        elif preheader.version == 2:
            bc_version = 2.1
        else:
            raise Exception("Unsupported bytecode version: " + str(bc_version))

        ljdcore.set_luajit_version(bc_version)

    header, prototype = ljd.rawdump.parser.parse(filename, on_parse_header)

    ast = ljd.ast.builder.build(header, prototype)
    assert ast is not None
    ljd.ast.validator.validate(ast, warped=True)

    return ast


if __name__ == '__main__':
    main()
