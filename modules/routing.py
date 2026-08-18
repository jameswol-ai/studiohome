"""
studiohome
Quick-action routing
"""

from __future__ import annotations

from typing import Any, Mapping


# =====================================================
# QUICK-ACTION ROUTES
# =====================================================

QUICK_ACTION_ROUTES: dict[str, str] = {
    "zoning_audit": "Zoning Code",
    "full_simulation": "Full Sim",
    "export_bim": "Export Suite",
}


# =====================================================
# ROUTE LOOKUP
# =====================================================

def get_quick_action_route(
    action: str,
) -> str | None:
    """
    Return the destination registered for a quick action.

    Returns None if the action is not registered.
    """

    return QUICK_ACTION_ROUTES.get(action)


# =====================================================
# ROUTE VALIDATION
# =====================================================

def validate_quick_action_route(
    action: str,
    module_mapping: Mapping[str, Any],
    flat_tab_labels: list[str] | tuple[str, ...],
) -> tuple[bool, str | None, str | None]:
    """
    Validate a quick-action route against the live module
    registry.

    Returns:

        (
            valid,
            destination,
            error_message,
        )
    """

    destination = get_quick_action_route(action)

    # -------------------------------------------------
    # Missing route
    # -------------------------------------------------

    if destination is None:

        return (
            False,
            None,
            (
                f"No quick-action route is registered "
                f"for '{action}'."
            ),
        )

    # -------------------------------------------------
    # Missing tab
    # -------------------------------------------------

    if destination not in flat_tab_labels:

        return (
            False,
            destination,
            (
                f"Quick-action '{action}' points to "
                f"'{destination}', but that destination "
                "is not registered in flat_tab_labels."
            ),
        )

    # -------------------------------------------------
    # Missing module mapping
    # -------------------------------------------------

    if destination not in module_mapping:

        return (
            False,
            destination,
            (
                f"Quick-action '{action}' points to "
                f"'{destination}', but that destination "
                "is missing from module_mapping."
            ),
        )

    # -------------------------------------------------
    # Empty module mapping
    # -------------------------------------------------

    if module_mapping[destination] is None:

        return (
            False,
            destination,
            (
                f"Quick-action '{action}' points to "
                f"'{destination}', but its module mapping "
                "is None."
            ),
        )

    # -------------------------------------------------
    # Valid
    # -------------------------------------------------

    return (
        True,
        destination,
        None,
    )