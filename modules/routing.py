"""
studiohome application routing.

Pure-Python routing helpers used by the Executive Cockpit
and other UI layers.

This module must not import Streamlit.
"""

from __future__ import annotations


QUICK_ACTION_ROUTES: dict[str, str] = {
    "zoning_audit": "Zoning Code",
    "full_simulation": "Full Sim",
    "export_bim": "Export Suite",
}


def get_quick_action_route(action: str) -> str | None:
    """
    Return the destination module for a Cockpit quick action.

    Returns None when the action is not registered.
    """
    return QUICK_ACTION_ROUTES.get(action)