"""
Verify registered modules are safe to import without Streamlit.

Each module is imported in an isolated subprocess. The subprocess
installs a fake Streamlit module that raises on import/API access.

This prevents streamlit_app.py or Streamlit UI setup from being
executed as a side effect of importing a module.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from modules.registry import MODULE_DEFINITIONS


PROJECT_ROOT = Path(__file__).resolve().parents[1]


SUBPROCESS_SCRIPT = r"""
import builtins
import sys
import types


class StreamlitImportViolation(RuntimeError):
    pass


class StreamlitGuard(types.ModuleType):
    def __getattr__(self, name):
        raise StreamlitImportViolation(
            f"Streamlit API accessed during module import: st.{name}"
        )


def blocked_import(
    name,
    globals=None,
    locals=None,
    fromlist=(),
    level=0,
):
    root = name.split(".", 1)[0]

    if root == "streamlit":
        raise StreamlitImportViolation(
            f"Module imported Streamlit during import: {name}"
        )

    return original_import(
        name,
        globals,
        locals,
        fromlist,
        level,
    )


original_import = builtins.__import__

builtins.__import__ = blocked_import

streamlit_guard = StreamlitGuard("streamlit")

sys.modules["streamlit"] = streamlit_guard

module_name = sys.argv[1]

try:
    __import__(module_name)

except StreamlitImportViolation as exc:
    print(f"STREAMLIT_VIOLATION: {exc}", file=sys.stderr)
    raise SystemExit(2)

except Exception as exc:
    print(
        f"IMPORT_FAILURE: {type(exc).__name__}: {exc}",
        file=sys.stderr,
    )
    raise SystemExit(1)

else:
    print(f"OK: {module_name}")
"""


@pytest.mark.parametrize(
    "definition",
    MODULE_DEFINITIONS,
    ids=lambda definition: definition.name,
)
def test_registered_module_imports_without_streamlit(definition):
    """Every registered module must be import-safe without Streamlit."""

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
            f"{definition.name} imports or accesses Streamlit "
            f"during module import:\n"
            f"{result.stderr.strip()}"
        )

    if result.returncode != 0:
        pytest.fail(
            f"{definition.name} failed to import in isolation:\n"
            f"{result.stderr.strip()}"
        )

    assert result.stdout.strip() == (
        f"OK: {definition.import_path}"
    )