"""
Import-side-effect contract tests for studiohome modules.

Every registered module is imported in a fresh Python subprocess.

The subprocess blocks and reports:

- file writes / filesystem mutation
- environment mutation
- subprocess creation
- socket creation / connection
- database client initialization
- unexpected stdout
- unexpected stderr

The test deliberately does NOT import streamlit_app.py.
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
import socket
import subprocess
import sys
import types


MODULE_NAME = sys.argv[1]


# =====================================================
# DIAGNOSTIC FAILURE
# =====================================================

class ImportSideEffectViolation(RuntimeError):
    """Raised when module import performs a blocked operation."""


def blocked(category: str, operation: str):
    raise ImportSideEffectViolation(
        f"IMPORT_SIDE_EFFECT [{category}] "
        f"module={MODULE_NAME!r} "
        f"operation={operation}"
    )


# =====================================================
# FILESYSTEM GUARDS
# =====================================================

_original_open = builtins.open
_original_path_open = pathlib.Path.open


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
        blocked(
            "FILESYSTEM",
            f"open({file!r}, mode={mode!r})",
        )

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
        blocked(
            "FILESYSTEM",
            f"Path.open({self!r}, mode={mode!r})",
        )

    return _original_path_open(
        self,
        mode,
        *args,
        **kwargs,
    )


def guarded_write_text(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.write_text({self!r})",
    )


def guarded_write_bytes(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.write_bytes({self!r})",
    )


def guarded_touch(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.touch({self!r})",
    )


def guarded_mkdir(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.mkdir({self!r})",
    )


def guarded_rmdir(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.rmdir({self!r})",
    )


def guarded_unlink(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.unlink({self!r})",
    )


def guarded_rename(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.rename({self!r})",
    )


def guarded_replace(self, *args, **kwargs):
    blocked(
        "FILESYSTEM",
        f"Path.replace({self!r})",
    )


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
# ENVIRONMENT GUARDS
# =====================================================

_original_putenv = os.putenv
_original_unsetenv = os.unsetenv


def guarded_putenv(key, value):
    blocked(
        "ENVIRONMENT",
        f"os.putenv({key!r}, ...)",
    )


def guarded_unsetenv(key):
    blocked(
        "ENVIRONMENT",
        f"os.unsetenv({key!r})",
    )


os.putenv = guarded_putenv
os.unsetenv = guarded_unsetenv


_original_environ_setitem = os._Environ.__setitem__
_original_environ_delitem = os._Environ.__delitem__


def guarded_environ_setitem(self, key, value):
    blocked(
        "ENVIRONMENT",
        f"os.environ[{key!r}] = ...",
    )


def guarded_environ_delitem(self, key):
    blocked(
        "ENVIRONMENT",
        f"del os.environ[{key!r}]",
    )


os._Environ.__setitem__ = guarded_environ_setitem
os._Environ.__delitem__ = guarded_environ_delitem


# =====================================================
# SUBPROCESS GUARDS
# =====================================================

_original_popen = subprocess.Popen
_original_run = subprocess.run
_original_call = subprocess.call
_original_check_call = subprocess.check_call
_original_check_output = subprocess.check_output
_original_getoutput = subprocess.getoutput
_original_getstatusoutput = subprocess.getstatusoutput


def guarded_popen(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.Popen(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_run(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.run(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_call(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.call(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_check_call(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.check_call(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_check_output(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.check_output(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_getoutput(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.getoutput(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_getstatusoutput(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"subprocess.getstatusoutput(args={args!r}, kwargs={kwargs!r})",
    )


subprocess.Popen = guarded_popen
subprocess.run = guarded_run
subprocess.call = guarded_call
subprocess.check_call = guarded_check_call
subprocess.check_output = guarded_check_output
subprocess.getoutput = guarded_getoutput
subprocess.getstatusoutput = guarded_getstatusoutput


def guarded_system(command):
    blocked(
        "SUBPROCESS",
        f"os.system({command!r})",
    )


def guarded_spawnv(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"os.spawnv(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_spawnve(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"os.spawnve(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_spawnvp(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"os.spawnvp(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_spawnvpe(*args, **kwargs):
    blocked(
        "SUBPROCESS",
        f"os.spawnvpe(args={args!r}, kwargs={kwargs!r})",
    )


os.system = guarded_system
os.spawnv = guarded_spawnv
os.spawnve = guarded_spawnve
os.spawnvp = guarded_spawnvp
os.spawnvpe = guarded_spawnvpe


# =====================================================
# SOCKET GUARDS
# =====================================================

_original_socket = socket.socket
_original_create_connection = socket.create_connection
_original_create_server = socket.create_server


class GuardedSocket:
    """
    Wrapper used to catch both socket creation and connect().
    """

    def __init__(self, *args, **kwargs):
        blocked(
            "SOCKET",
            f"socket.socket(args={args!r}, kwargs={kwargs!r})",
        )


def guarded_socket(*args, **kwargs):
    blocked(
        "SOCKET",
        f"socket.socket(args={args!r}, kwargs={kwargs!r})",
    )


def guarded_create_connection(*args, **kwargs):
    blocked(
        "SOCKET",
        f"socket.create_connection("
        f"args={args!r}, kwargs={kwargs!r})",
    )


def guarded_create_server(*args, **kwargs):
    blocked(
        "SOCKET",
        f"socket.create_server("
        f"args={args!r}, kwargs={kwargs!r})",
    )


socket.socket = guarded_socket
socket.create_connection = guarded_create_connection
socket.create_server = guarded_create_server


# =====================================================
# DATABASE CLIENT GUARDS
# =====================================================

def database_blocked_factory(database_name: str):
    def factory(*args, **kwargs):
        blocked(
            "DATABASE",
            f"{database_name}("
            f"args={args!r}, kwargs={kwargs!r})",
        )

    return factory


# -----------------------------------------------------
# sqlite3
# -----------------------------------------------------

try:
    import sqlite3

    sqlite3.connect = database_blocked_factory(
        "sqlite3.connect"
    )

except ImportError:
    pass


# -----------------------------------------------------
# psycopg / psycopg2
# -----------------------------------------------------

try:
    import psycopg

    psycopg.connect = database_blocked_factory(
        "psycopg.connect"
    )

except ImportError:
    pass


try:
    import psycopg2

    psycopg2.connect = database_blocked_factory(
        "psycopg2.connect"
    )

except ImportError:
    pass


# -----------------------------------------------------
# MySQL
# -----------------------------------------------------

try:
    import mysql.connector

    mysql.connector.connect = database_blocked_factory(
        "mysql.connector.connect"
    )

except ImportError:
    pass


try:
    import pymysql

    pymysql.connect = database_blocked_factory(
        "pymysql.connect"
    )

except ImportError:
    pass


# -----------------------------------------------------
# SQLAlchemy
# -----------------------------------------------------

try:
    import sqlalchemy

    sqlalchemy.create_engine = database_blocked_factory(
        "sqlalchemy.create_engine"
    )

except ImportError:
    pass


# -----------------------------------------------------
# MongoDB
# -----------------------------------------------------

try:
    import pymongo

    pymongo.MongoClient = database_blocked_factory(
        "pymongo.MongoClient"
    )

except ImportError:
    pass


# =====================================================
# STDOUT / STDERR GUARDS
# =====================================================

class GuardedStream:
    def __init__(self, original, name):
        self.original = original
        self.name = name

    def write(self, data):
        if data:
            blocked(
                "OUTPUT",
                f"unexpected {self.name}: {data!r}",
            )

        return 0

    def flush(self):
        return self.original.flush()

    def isatty(self):
        return False

    def __getattr__(self, name):
        return getattr(self.original, name)


sys.stdout = GuardedStream(
    sys.stdout,
    "stdout",
)

sys.stderr = GuardedStream(
    sys.stderr,
    "stderr",
)


# =====================================================
# IMPORT
# =====================================================

try:
    __import__(MODULE_NAME)

except ImportSideEffectViolation as exc:

    # Restore the streams before emitting diagnostics.
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print(
        str(exc),
        file=sys.stderr,
    )

    raise SystemExit(2)

except Exception as exc:

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print(
        f"IMPORT_FAILURE "
        f"module={MODULE_NAME!r} "
        f"error={type(exc).__name__}: {exc}",
        file=sys.stderr,
    )

    raise SystemExit(1)

else:

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print(
        f"OK: {MODULE_NAME}"
    )
"""


@pytest.mark.parametrize(
    "definition",
    MODULE_DEFINITIONS,
    ids=lambda definition: definition.name,
)
def test_registered_module_has_no_import_side_effects(
    definition,
):
    """
    Every registered module must import without causing
    filesystem, environment, subprocess, socket, database,
    stdout, or stderr side effects.
    """

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

    if result.returncode == 2:
        pytest.fail(
            f"\n{definition.name} has a blocked "
            f"import-time side effect.\n\n"
            f"{result.stderr.strip()}"
        )

    if result.returncode != 0:
        pytest.fail(
            f"\n{definition.name} failed during "
            f"isolated import.\n\n"
            f"{result.stderr.strip()}"
        )

    assert result.stdout.strip() == (
        f"OK: {definition.import_path}"
    )

    assert result.stderr.strip() == ""