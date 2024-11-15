from test.testunit import Mode, Test

tests = [
    # Very trivial testcases, more for testing the test framework than the decompiler
    Test("simple", Mode.MATCHES),
    Test("loops", Mode.MATCHES),
    Test("massive_nils", Mode.BCDIFF_MATCHES),  # Massive nil expansion very often breaks byte-for-byte comparisons
    Test("massive_std", Mode.MATCHES),
    Test("illegal_type_eliminations", Mode.MATCHES),
    Test("slot_local_declarations", Mode.MATCHES),
    Test("slot_block_gathering", Mode.MATCHES),
    Test("arguments", Mode.MATCHES),
    Test("complex_expressions", Mode.MATCHES),
    Test("upvalues", Mode.MATCHES),
    Test("weird_bytecode_expression", Mode.MATCHES),  # It's probably okay to bump this down to DECOMPILES temporarily
    Test("side_effect_reordering", Mode.MATCHES),
    Test("scoped_table_constructor", Mode.MATCHES),
    Test("string_encoding", Mode.MATCHES),
    Test("upvalues_loops", Mode.MATCHES),
    Test("upvalues_blocks", Mode.MATCHES),
    Test("reused_loop_controls", Mode.MATCHES),
    Test("expression_loop_jump_over", Mode.MATCHES),
    Test("self_arg", Mode.MATCHES),
    Test("expression_dummy_ignoring", Mode.MATCHES),
    Test("upvalues_nested", Mode.MATCHES),
    Test("subexpression_simple", Mode.BCDIFF_MATCHES),
    Test("nil_object_reuse", Mode.MATCHES),

    # The old (pre test framework) tests
    Test("old/breaks", Mode.BCDIFF_MATCHES),
    Test("old/expression", Mode.BCDIFF_MATCHES),
    Test("old/ifs", Mode.BCDIFF_MATCHES),
    Test("old/loop", Mode.BCDIFF_MATCHES),
    Test("old/operations", Mode.BCDIFF_MATCHES),
    Test("old/primitive", Mode.BCDIFF_MATCHES),
]
