from typing import List

import ljd.ast.nodes as nodes
import ljd.ast.traverse as traverse
import ljd.ast.slotfinder as slotfinder
import ljd.ast.mutator as mutator

import bcdiff.blockchecker
from bcdiff.types import BlockInfo


def compare_ast(a: nodes.FunctionDefinition, b: nodes.FunctionDefinition):
    _preprocess(a)
    _preprocess(b)

    func_a = _FunctionFinder.find(a)
    func_b = _FunctionFinder.find(b)

    assert len(func_a) == len(func_b)

    for af, bf in zip(func_a, func_b):
        _compare_functions(af, bf)


def _preprocess(func: nodes.FunctionDefinition):
    # Run the mutator on the function. This certainly isn't ideal either (see
    # below), but it fixes up stuff like where the loops are (required for the
    # slotfinder) adds the implicit assignments from ISTC/ISFC.
    mutator.pre_pass(func)

    # It's not ideal, but run SlotFinder over these functions to setup slot IDs for
    # all the identifiers, which we'll later use to determine if something is the
    # same even if the slot numbers changed.
    # This means that if there's a bug in slotfinder, it could potentially mask itself
    # in tests that use bcdiff, applying both to the decompiler and differ. This is
    # why it's important to have lots of tests that use bytecode equality, or at least
    # some mode in bcdiff to turn this off.
    slotfinder.process(func)


def _compare_functions(a: nodes.FunctionDefinition, b: nodes.FunctionDefinition):
    assert len(a.statements.contents) == len(b.statements.contents)

    state = bcdiff.blockchecker.CompareState()

    bcdiff.blockchecker.compare_func_meta(a, b, state)

    ai = _prepare_function(a)
    bi = _prepare_function(b)

    for block_a, block_b in zip(a.statements.contents, b.statements.contents):
        bcdiff.blockchecker.compare_blocks(block_a, ai, block_b, bi, state)


def _prepare_function(function: nodes.FunctionDefinition) -> BlockInfo:
    blocks: List[nodes.Block] = function.statements.contents

    for block in blocks:
        assert isinstance(block, nodes.Block)
        block.warpins = []

    for block in blocks:
        for tgt in _get_warp_targets(block.warp):
            tgt.warpins.append(block)

    for block in blocks:
        block.warpins_count = len(block.warpins)

    info = BlockInfo(function)
    return info


def _get_warp_targets(warp) -> List[nodes.Block]:
    if isinstance(warp, nodes.UnconditionalWarp):
        return [warp.target]
    elif isinstance(warp, nodes.ConditionalWarp):
        return [warp.true_target, warp.false_target]
    elif isinstance(warp, nodes.NumericLoopWarp) or isinstance(warp, nodes.IteratorWarp):
        return [warp.body, warp.way_out]
    else:
        assert isinstance(warp, nodes.EndWarp)
        return []


class _FunctionFinder(traverse.Visitor):
    functions: List[nodes.FunctionDefinition]

    @staticmethod
    def find(ast: nodes.FunctionDefinition):
        assert isinstance(ast, nodes.FunctionDefinition)
        ff = _FunctionFinder()
        traverse.traverse(ff, ast)
        return ff.functions

    def __init__(self):
        super().__init__()
        self.functions = []

    def visit_function_definition(self, node):
        self.functions.append(node)
