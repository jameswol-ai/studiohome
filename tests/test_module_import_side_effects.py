"""
Import-side-effect contract tests for studiohome modules.

Each registered module is imported in a fresh subprocess.

The subprocess rejects:
- file writes
- file deletion/renaming
- environment mutation
- unexpected stdout
- unexpected stderr

The test does NOT import streamlit_app.py.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from modules.registry import MODULE_DEFINITIONS


PROJECT_ROOT = Path(__file__).resolve().parents[1]


SUBPROCESS_SCRIPT = r"""
from __future__ import annotations

import builtins
import os
import pathlib
import sys


module_name = sys.argv[1]


# =====================================================
# FILE-SYSTEM WRITE GUARDS
# =====================================================

_original_open = builtins.open
_original_path_open = pathlib.Path.open
_original_path_write_text = pathlib.Path.write_text
_original_path_write_bytes = pathlib.Path.write_bytes
_original_path_touch = pathlib.Path.touch
_original_path_mkdir = pathlib.Path.mkdir
_original_path_rmdir = pathlib.Path.rmdir
_original_path_unlink = pathlib.Path.unlink
_original_path_rename = pathlib.Path.rename
_original_path_replace = pathlib.Path.replace


def fail(operation):
    raise RuntimeError(
        f"IMPORT_SIDE_EFFECT: file operation blocked: {operation}"
    )


def guarded_open(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    if any(flag in mode for flag in ("w", "a", "x", "+")):
        fail(f"open({file!r}, mode={mode!r})")

    return _original_open(
        file,
        mode,
        buffering,
        encoding,
        errors,
        newline,
        closefd,
        opener,
    )


def guarded_path_open(self, mode="r", *args, **kwargs):
    if any(flag in mode for flag in ("w", "a", "x", "+")):
        fail(f"Path.open({self!r}, mode={mode!r})")

    return _original_path_open(
        self,
        mode,
        *args,
        **kwargs,
    )


def guarded_write_text(self, *args, **kwargs):
    fail(f"Path.write_text({self!r})")


def guarded_write_bytes(self, *args, **kwargs):
    fail(f"Path.write_bytes({self!r})")


def guarded_touch(self, *args, **kwargs):
    fail(f"Path.touch({self!r})")


def guarded_mkdir(self, *args, **kwargs):
    fail(f"Path.mkdir({self!r})")


def guarded_rmdir(self, *args, **kwargs):
    fail(f"Path.rmdir({self!r})")


def guarded_unlink(self, *args, **kwargs):
    fail(f"Path.unlink({self!r})")


def guarded_rename(self, *args, **kwargs):
    fail(f"Path.rename({self!r})")


def guarded_replace(self, *args, **kwargs):
    fail(f"Path.replace({self!r})")


builtins.open = guarded_open
pathlib.Path.open = guarded_path_open
pathlib.Path.write_text = guarded_write_text
pathlib.Path.write_bytes = guarded_write_bytes
pathlib.Path.touch = guarded_touch
pathlib.Path.mkdir = guarded_mkdir
pathlib.Path.rmdir = guarded_rmdir
pathlib.Path.unlink = guarded_unlink
pathlib.Path.rename = guarded_rename
pathlib.Path.replace = guarded_replace


# =====================================================
# ENVIRONMENT MUTATION GUARDS
# =====================================================

_original_putenv = os.putenv
_original_unsetenv = os.unsetenv


def guarded_putenv(key, value):
    fail(f"os.putenv({key!r}, ...)")


def guarded_unsetenv(key):
    fail(f"os.unsetenv({key!r})")


_original_environ_setitem = os._Environ.__setitem__
_original_environ_delitem = os._Environ.__delitem__


def guarded_environ_setitem(self, key, value):
    fail(f"os.environ[{key!r}] = ...")


def guarded_environ_delitem(self, key):
    fail(f"del os.environ[{key!r}]")


os.putenv = guarded_putenv
os.unsetenv = guarded_unsetenv
os._Environ.__setitem__ = guarded_environ_setitem
os._Environ.__delitem__ = guarded_environ_delitem


# =====================================================
# STDOUT / STDERR GUARDS
# =====================================================

class GuardedStream:
    def __init__(self, original, name):
        self.original = original
        self.name = name

    def write(self, data):
        if data:
            raise RuntimeError(
                f"IMPORT_SIDE_EFFECT: unexpected {self.name}: "
                f"{data!r}"
            )

        return 0

    def flush(self):
        return self.original.flush()

    def isatty(self):
        return False

    def __getattr__(self, name):
        return getattr(self.original, name)


sys.stdout = GuardedStream(sys.stdout, "stdout")
sys.stderr = GuardedStream(sys.stderr, "stderr")


# =====================================================
# IMPORT MODULE
# =====================================================

try:
    __import__(module_name)

except Exception as exc:
    # Restore normal streams so pytest can receive the
    # actual diagnostic from the subprocess.
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print(
        f"{type(exc).__name__}: {exc}",
        file=sys.stderr,
    )

    raise SystemExit(1)

else:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print(f"OK: {module_name}")
"""


@pytest.mark.parametrize(
    "definition",
    MODULE_DEFINITIONS,
    ids=lambda definition: definition.name,
)
def test_registered_module_has_no_import_side_effects(definition):
    """Registered modules must be side-effect-free at import time."""

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            SUBPROCESS_SCRIPT,
            definition.import_path,
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        pytest.fail(
            f"{definition.name} produced an import-time "
            "side effect or failed to import.\n\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    assert result.stdout.strip() == (
        f"OK: {definition.import_path}"
    )

    assert result.stderr.strip() == ""