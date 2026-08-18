"""
studiohome
Quick-action routing
"""

from __future__ import annotations

from typing import Any, Mapping


QUICK_ACTION_ROUTES: dict[str, str] = {
    "zoning_audit": "Zoning Code",
    "full_simulation": "Full Sim",
    "export_bim": "Export Suite",
}


def get_quick_action_route(
    action: str,
) -> str | None:
    """Return the destination for a registered action."""
    return QUICK_ACTION_ROUTES.get(action)


def validate_quick_action_route(
    action: str,
    module_mapping: Mapping[str, Any],
    flat_tab_labels: list[str] | tuple[str, ...],
) -> tuple[bool, str | None, str | None]:
    """
    Validate a quick-action destination against the
    application's live module registry.
    """

    destination = get_quick_action_route(action)

    if destination is None:
        return (
            False,
            None,
            f"No quick-action route is registered for '{action}'.",
        )

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

    return True, destination, None