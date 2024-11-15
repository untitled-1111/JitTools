#!/usr/bin/env python3
import pathlib
import tempfile
from argparse import ArgumentParser

from test.config import Config
from test.testunit import Test, Mode, TestResult
from test.testlist import tests as all_tests
from test.utils import Colour


def main():
    parser = ArgumentParser()

    parser.add_argument("tests", metavar="test", type=str, nargs="+", help="Names of tests to be run, or 'all'")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print per-test information")
    parser.add_argument("--wait", action="store_true", help="Once the tests are complete, wait for user input before "
                                                            "deleting the artifacts")
    parser.add_argument("--ljd-opt", action="append", type=str, dest="ljd_opt", default=[],
                        help="Arguments to be passed to the decompiler, use multiple times for multiple arguments")

    args = parser.parse_args()

    config = Config()
    config.ljd_args = args.ljd_opt
    config.verbose = args.verbose

    by_name = dict()
    for test in all_tests:
        by_name[test.name] = test

    if args.tests == ["all"]:
        args.tests = sorted(by_name)

    for i, s in enumerate(args.tests):
        if not s.startswith("dyn:"):
            continue

        parts = s.split(":")
        assert len(parts) == 3

        name = "__custom_%d" % i
        args.tests[i] = name
        by_name[name] = Test(parts[1], getattr(Mode, parts[2]))

    tempdir = tempfile.TemporaryDirectory(prefix="ljd-test-")

    for name in args.tests:
        test = by_name[name]
        result = test.test(config, pathlib.Path(tempdir.name))

        if result == TestResult.PASS:
            Colour.GREEN.write("[*] PASS ")
        elif result == TestResult.FAIL:
            Colour.RED.write("[x] FAIL ")
        else:
            assert result == TestResult.ERROR
            Colour.RED.set_bg()
            Colour.WHITE.write("[!]")
            Colour.RED.write(" ERR  ")

        print(name)

    if args.wait:
        input("Press enter to continue, files at %s " % tempdir.name)


if __name__ == "__main__":
    main()
