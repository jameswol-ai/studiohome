"""Shared deterministic parametric design state for the studiohome modules."""
from __future__ import annotations

import math
from typing import Any


def _safe(value: Any, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _grid_count(length: float, spacing: float) -> int:
    return max(1, int(math.ceil(length / max(spacing, 0.1))))


def build_design_state(
    project: dict[str, Any],
    *,
    family: str | None = None,
    typology: str | None = None,
    site_area: float | None = None,
    floors: int | None = None,
    grid_spacing: float | None = None,
    floor_to_floor: float | None = None,
    coverage: float | None = None,
    unit_rate: float | None = None,
    core_ratio: float | None = None,
    window_wall_ratio: float | None = None,
) -> dict[str, Any]:
    """Build a deterministic geometry, quantity and program state."""
    family = family or str(project.get("design_family", "Commercial"))
    typology = typology or str(project.get("typology", "Office Building"))
    site = max(200.0, _safe(site_area if site_area is not None else project.get("site_area"), 2500.0))
    storeys = max(1, int(floors if floors is not None else project.get("floors", 10)))
    grid = max(4.0, _safe(grid_spacing if grid_spacing is not None else project.get("grid_spacing"), 8.0))
    floor_height = max(2.7, _safe(floor_to_floor if floor_to_floor is not None else project.get("floor_to_floor"), 3.5))

    default_coverage = {"Residential": 0.38, "Commercial": 0.50, "Industrial": 0.60}.get(family, 0.50)
    coverage = min(0.90, max(0.10, _safe(coverage if coverage is not None else project.get("site_coverage"), default_coverage)))
    footprint = site * coverage
    gfa = footprint * storeys

    # Keep proportions stable and suitable for 2D plans across building scales.
    aspect = {"Residential": 1.20, "Commercial": 1.45, "Industrial": 1.80}.get(family, 1.45)
    width = math.sqrt(footprint * aspect)
    depth = footprint / max(width, 1.0)
    bays_x = _grid_count(width, grid)
    bays_y = _grid_count(depth, grid)
    actual_grid_x = width / bays_x
    actual_grid_y = depth / bays_y

    core_ratio = min(0.30, max(0.05, _safe(core_ratio if core_ratio is not None else project.get("core_ratio"), {"Residential": 0.12, "Commercial": 0.15, "Industrial": 0.08}.get(family, 0.12))))
    core_area = gfa * core_ratio
    circulation_ratio = {"Residential": 0.14, "Commercial": 0.12, "Industrial": 0.10}.get(family, 0.12)
    circulation_area = gfa * circulation_ratio
    net_program_area = max(0.0, gfa - core_area - circulation_area)

    wwr = min(0.85, max(0.10, _safe(window_wall_ratio if window_wall_ratio is not None else project.get("window_wall_ratio"), {"Residential": 0.45, "Commercial": 0.55, "Industrial": 0.25}.get(family, 0.45))))
    perimeter = 2.0 * (width + depth)
    envelope_area = perimeter * storeys * floor_height
    window_area = envelope_area * wwr
    roof_area = footprint
    building_height = storeys * floor_height
    far = gfa / site
    structural_grid_intersections = (bays_x + 1) * (bays_y + 1)
    column_count = max(4, structural_grid_intersections - max(4, int(core_area / max(grid * grid, 1.0))))

    rate = max(0.0, _safe(unit_rate if unit_rate is not None else project.get("unit_rate"), {"Residential": 1450.0, "Commercial": 1750.0, "Industrial": 1250.0}.get(family, 1650.0)))
    estimated_cost = gfa * rate

    program = {
        "Residential": [("Residential Units", 0.68), ("Circulation", 0.14), ("Core", core_ratio), ("Amenity", 0.06)],
        "Commercial": [("Work / Retail", 0.63), ("Circulation", 0.12), ("Core", core_ratio), ("Amenities", 0.10)],
        "Industrial": [("Production / Storage", 0.72), ("Circulation", 0.10), ("Services", 0.08), ("Administration", 0.10)],
    }.get(family, [("Program", 1.0)])
    shares = [share for _, share in program]
    total_share = sum(shares)
    program_schedule = [(name, share / total_share, gfa * share / total_share) for name, share in program]

    return {
        "design_family": family,
        "typology": typology,
        "site_area": site,
        "site_coverage": coverage,
        "floors": storeys,
        "floor_to_floor": floor_height,
        "grid_spacing": grid,
        "floorplate_width": width,
        "floorplate_depth": depth,
        "footprint_area": footprint,
        "total_gfa": gfa,
        "building_height": building_height,
        "far": far,
        "grid_bays_x": bays_x,
        "grid_bays_y": bays_y,
        "actual_grid_spacing_x": actual_grid_x,
        "actual_grid_spacing_y": actual_grid_y,
        "structural_grid_intersections": structural_grid_intersections,
        "column_count": column_count,
        "core_ratio": core_ratio,
        "core_area": core_area,
        "circulation_area": circulation_area,
        "net_program_area": net_program_area,
        "perimeter": perimeter,
        "envelope_area": envelope_area,
        "window_wall_ratio": wwr,
        "window_area": window_area,
        "roof_area": roof_area,
        "unit_rate": rate,
        "estimated_cost": estimated_cost,
        "program_schedule": program_schedule,
    }


def apply_design_state(project: dict[str, Any], state: dict[str, Any], *, status: str = "Concept Generated") -> dict[str, Any]:
    """Apply generated values to the shared project dictionary in-place."""
    project.update(state)
    project["design_revision"] = int(project.get("design_revision", 0)) + 1
    project["design_status"] = status
    return project


def get_program_schedule(project: dict[str, Any]):
    """Return the current program schedule as simple records."""
    return project.get("program_schedule", [])
