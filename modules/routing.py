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

    Returns None when the action does not exist.
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

    Validation requires the destination to:

    1. Have a configured quick-action route.
    2. Exist in flat_tab_labels.
    3. Exist in module_mapping.
    4. Have a non-None module mapping.
    """

    # -------------------------------------------------
    # Route lookup
    # -------------------------------------------------

    destination = get_quick_action_route(action)

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
    # flat_tab_labels validation
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
    # module_mapping validation
    # -------------------------------------------------

    if destination not in module_mapping:
        return (
            False,
            destination,
            (
                f"Quick-action '{action}' points to "
                f"'{destination}', but no module is "
                "registered in module_mapping."
            ),
        )

    # -------------------------------------------------
    # None module validation
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