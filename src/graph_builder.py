"""Campus graph construction utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx


def _import_osmnx() -> Any:
    try:
        import osmnx as ox
    except ImportError as exc:  # pragma: no cover - depends on environment setup
        raise RuntimeError("osmnx is required to build the campus walking graph.") from exc
    return ox


def _import_shapely_geometry() -> tuple[Any, Any, Any]:
    try:
        from shapely.geometry import MultiPolygon, Polygon, shape
    except ImportError as exc:  # pragma: no cover - depends on environment setup
        raise RuntimeError("shapely is required to parse boundary polygon geometry.") from exc
    return MultiPolygon, Polygon, shape


def _extract_geometry(payload: dict[str, Any]) -> dict[str, Any] | None:
    payload_type = payload.get("type")
    if payload_type == "FeatureCollection":
        features = payload.get("features") or []
        if not features:
            return None
        first_feature = features[0] or {}
        return first_feature.get("geometry")
    if payload_type == "Feature":
        return payload.get("geometry")
    if payload_type in {"Polygon", "MultiPolygon"}:
        return payload
    return payload.get("geometry")


def _load_boundary_polygon(polygon_geojson_path: str) -> Any:
    boundary_path = Path(polygon_geojson_path)
    if not boundary_path.exists():
        raise FileNotFoundError(f"Boundary file does not exist: {boundary_path}")

    payload = json.loads(boundary_path.read_text(encoding="utf-8"))
    geometry = _extract_geometry(payload)
    if geometry is None:
        raise ValueError("No polygon geometry found in boundary file.")

    multipolygon_cls, polygon_cls, shape = _import_shapely_geometry()
    polygon = shape(geometry)
    if polygon.is_empty:
        raise ValueError("Boundary geometry is empty.")
    if isinstance(polygon, multipolygon_cls):
        polygon = max(polygon.geoms, key=lambda geom: geom.area)
    if not isinstance(polygon, polygon_cls):
        raise ValueError("Boundary geometry must be Polygon or MultiPolygon.")

    return polygon


def _has_missing_edge_lengths(graph: nx.MultiDiGraph) -> bool:
    return any(edge_data.get("length") is None for _, _, _, edge_data in graph.edges(keys=True, data=True))


def _normalise_edge_distances(graph: nx.MultiDiGraph) -> None:
    for _, _, _, edge_data in graph.edges(keys=True, data=True):
        if edge_data.get("length") is None:
            raise ValueError("Graph contains edges without length after normalization.")
        length_m = float(edge_data["length"])
        if length_m <= 0:
            raise ValueError(f"Edge length must be positive, got {length_m}.")
        edge_data["distance_m"] = length_m


def build_walking_graph_from_polygon(polygon_geojson_path: str) -> nx.MultiDiGraph:
    """Load a campus boundary GeoJSON and fetch the walking graph from OSMnx.

    Every edge receives a normalized ``distance_m`` value sourced from OSMnx
    edge ``length`` (meters).
    """
    polygon = _load_boundary_polygon(polygon_geojson_path)
    ox = _import_osmnx()
    graph = ox.graph_from_polygon(polygon, network_type="walk", simplify=True)
    if graph.number_of_edges() == 0:
        raise ValueError("OSMnx returned an empty walking graph for the provided boundary.")

    if _has_missing_edge_lengths(graph):
        graph = ox.distance.add_edge_lengths(graph)

    _normalise_edge_distances(graph)
    return graph
