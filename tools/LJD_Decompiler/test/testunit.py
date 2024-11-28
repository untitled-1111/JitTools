import subprocess
import sys
from enum import Enum
from pathlib import Path

from test.utils import Colour

test_dir = Path(__file__).resolve().parent / "tests"


class Mode(Enum):
    """The levels to which a test must pass"""

    PARTIAL_FAILURE = 1
    """The file decompiles with --catch_asserts - should only be used to test error handling"""

    DECOMPILES = 2
    """The file decompiles successfully, but no checks are made against the input"""

    MATCHES = 3
    """The file decompiles, and it's re-compiled output matches the original bytecode"""

    RECOMPILES = 4
    """The file decompiles, and is successfully recompiled, though no checks are made against the input"""

    # noinspection SpellCheckingInspection
    BCDIFF_MATCHES = 5
    """The file decompiles, and bcdiff considers it's re-compiled output equal to the original bytecode"""


class TestResult(Enum):
    PASS = 1
    FAIL = 2
    ERROR = 3


class Test:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.src = Path(test_dir, "%s.lua" % name)

        self.bc_out = None
        self.src_out = None
        self.bc_out_recompiled = None

        assert self.src.is_file()

    def test(self, config, tmpdir):
        # noinspection PyBroadException
        try:
            return self._test_unsafe(config, tmpdir)
        except subprocess.CalledProcessError:
            return TestResult.FAIL
        except Exception:
            if config.verbose:
                raise
            return TestResult.ERROR

    def _test_unsafe(self, config, tmpdir):
        # TODO handle Mode.PARTIAL_FAILURE
        assert self.level != Mode.PARTIAL_FAILURE

        self.compile(config, False, tmpdir)
        self.decompile(config)

        if self.level == Mode.DECOMPILES:
            return TestResult.PASS

        self.recompile(config)

        if self.level == Mode.RECOMPILES:
            return TestResult.PASS

        if self.level == Mode.BCDIFF_MATCHES:
            equals = bc_diff(config, self.bc_out, self.bc_out_recompiled)
            return TestResult.PASS if equals else TestResult.FAIL

        with open(self.bc_out, "rb") as fi:
            bc1 = fi.read()

        with open(self.bc_out_recompiled, "rb") as fi:
            bc2 = fi.read()

        if bc1 != bc2:
            return TestResult.FAIL

        return TestResult.PASS

    def compile(self, config, symbols, tmpdir):
        self.bc_out = self._chkdir(tmpdir, "-orig.bc")
        self.src_out = self._chkdir(tmpdir, ".lua")
        self.bc_out_recompiled = self._chkdir(tmpdir, "-rc.bc")
        config.log("Compiling " + self.name + " to " + str(self.bc_out))
        lj_compile(config, self.src, self.bc_out, symbols)

    def decompile(self, config):
        assert self.bc_out
        config.log("Decompiling " + self.name)
        lj_decompile(config, self.bc_out, self.src_out, config.ljd_args)

    def recompile(self, config):
        assert self.bc_out
        config.log("Recompiling " + self.name)
        lj_compile(config, self.src_out, self.bc_out_recompiled, False)

    def _chkdir(self, tmpdir, ext):
        file = Path(tmpdir, self.name + ext)
        file.parent.mkdir(parents=True, exist_ok=True)
        return file


def lj_compile(config, input, output, symbols):
    args = ["luajit", "-b", "-t", "raw", str(input.resolve()), str(output.resolve())]
    if symbols:
        args[-1:-1] += ["-g"]
    cfg_run(config, args)


def lj_decompile(config, input, output, extra_args):
    main_file = Path(sys.argv[0]).resolve().parent / "main.py"
    args = ["python3", str(main_file), "-f", str(input), "-o", str(output)] + extra_args
    cfg_run(config, args)


def bc_diff(config, file1, file2) -> bool:
    main_file = Path(sys.argv[0]).resolve().parent / "bcdiff.py"
    args = ["python3", str(main_file), str(file1), str(file2)]
    proc = cfg_run(config, args)
    return proc.returncode == 0


def cfg_run(config, args):
    kwargs = {
        "args": args,
        "check": True,
    }

    if config.verbose:
        Colour.BLUE.set_fg()
    else:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL

    proc = subprocess.run(**kwargs)

    if config.verbose:
        Colour.reset()

    return proc
