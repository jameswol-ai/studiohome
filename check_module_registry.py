"""
Validate the studiohome module registry.

This script does not import streamlit_app.py, so it does
not execute Streamlit startup code.
"""

from modules.registry import validate_registry


def main() -> int:
    errors = validate_registry()

    if errors:
        print("MODULE REGISTRY CHECK FAILED")

        for error in errors:
            print(f"  - {error}")

        return 1

    print(
        "OK: all registered modules import successfully "
        "and expose callable render() functions."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())