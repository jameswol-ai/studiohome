"""
Tests for studiohome application routing.

These tests deliberately do not import Streamlit.
"""

from modules.routing import (
    QUICK_ACTION_ROUTES,
    get_quick_action_route,
)


def test_zoning_audit_routes_to_zoning_code():
    assert (
        get_quick_action_route("zoning_audit")
        == "Zoning Code"
    )


def test_full_simulation_routes_to_full_sim():
    assert (
        get_quick_action_route("full_simulation")
        == "Full Sim"
    )


def test_export_bim_routes_to_export_suite():
    assert (
        get_quick_action_route("export_bim")
        == "Export Suite"
    )


def test_unknown_action_returns_none():
    assert (
        get_quick_action_route("does_not_exist")
        is None
    )


def test_quick_action_routes_are_strings():
    for action, destination in QUICK_ACTION_ROUTES.items():
        assert isinstance(action, str)
        assert isinstance(destination, str)


def test_all_quick_actions_have_destinations():
    assert QUICK_ACTION_ROUTES == {
        "zoning_audit": "Zoning Code",
        "full_simulation": "Full Sim",
        "export_bim": "Export Suite",
    }