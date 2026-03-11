"""Campus graph construction utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx


SUPPORTED_BOUNDARY_GEOMETRY_TYPES = {"Polygon", "MultiPolygon"}


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


def _has_valid_polygon_coordinates(geometry_type: str, coordinates: Any) -> bool:
    if not isinstance(coordinates, list) or not coordinates:
        return False
    if geometry_type == "Polygon":
        return any(isinstance(ring, list) and len(ring) >= 4 for ring in coordinates)
    if geometry_type == "MultiPolygon":
        for polygon in coordinates:
            if not isinstance(polygon, list) or not polygon:
                continue
            if any(isinstance(ring, list) and len(ring) >= 4 for ring in polygon):
                return True
        return False
    return False


def _is_polygon_geometry_mapping(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    geometry_type = value.get("type")
    coordinates = value.get("coordinates")
    if geometry_type not in SUPPORTED_BOUNDARY_GEOMETRY_TYPES:
        return False
    return _has_valid_polygon_coordinates(geometry_type, coordinates)


def _extract_geometry(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, bool]:
    payload_type = payload.get("type")

    if payload_type == "FeatureCollection":
        features = payload.get("features")
        if not isinstance(features, list) or not features:
            return None, False

        saw_invalid_geometry = False
        for feature in features:
            if not isinstance(feature, dict) or feature.get("type") != "Feature":
                continue
            geometry = feature.get("geometry")
            if geometry is None:
                continue
            if _is_polygon_geometry_mapping(geometry):
                return geometry, False
            if isinstance(geometry, dict):
                saw_invalid_geometry = True
        return None, saw_invalid_geometry

    if payload_type == "Feature":
        geometry = payload.get("geometry")
        if geometry is None:
            return None, False
        if _is_polygon_geometry_mapping(geometry):
            return geometry, False
        return None, isinstance(geometry, dict)

    if payload_type in SUPPORTED_BOUNDARY_GEOMETRY_TYPES:
        if _is_polygon_geometry_mapping(payload):
            return payload, False
        return None, True

    return None, False


def _load_boundary_polygon(polygon_geojson_path: str) -> Any:
    boundary_path = Path(polygon_geojson_path)
    if not boundary_path.exists():
        raise FileNotFoundError(f"Boundary file does not exist: {boundary_path}")

    try:
        payload = json.loads(boundary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid boundary GeoJSON: file is not valid JSON.") from exc

    if not isinstance(payload, dict):
        raise ValueError("Invalid boundary GeoJSON: top-level value must be an object.")

    geometry, saw_invalid_geometry = _extract_geometry(payload)
    if geometry is None:
        if saw_invalid_geometry:
            raise ValueError("Boundary geometry is not a valid GeoJSON geometry.")
        raise ValueError("No polygon geometry found in boundary file.")

    multipolygon_cls, polygon_cls, shape = _import_shapely_geometry()
    try:
        polygon = shape(geometry)
    except Exception as exc:
        raise ValueError("Boundary geometry is not a valid GeoJSON geometry.") from exc

    if polygon.is_empty:
        raise ValueError("Boundary geometry is empty.")
    if not isinstance(polygon, (polygon_cls, multipolygon_cls)):
        raise ValueError("Boundary geometry must be Polygon or MultiPolygon.")

    return polygon


def _has_missing_edge_lengths(graph: nx.MultiDiGraph) -> bool:
    return any(edge_data.get("length") is None for _, _, _, edge_data in graph.edges(keys=True, data=True))


def _resolve_add_edge_lengths(ox: Any) -> Any:
    distance_module = getattr(ox, "distance", None)
    if distance_module is not None and hasattr(distance_module, "add_edge_lengths"):
        return distance_module.add_edge_lengths
    if hasattr(ox, "add_edge_lengths"):
        return ox.add_edge_lengths
    raise RuntimeError(
        "osmnx version does not expose add_edge_lengths; "
        "please upgrade osmnx or provide edge lengths."
    )


def _normalise_edge_distances(graph: nx.MultiDiGraph) -> None:
    for source, target, key, edge_data in graph.edges(keys=True, data=True):
        edge_label = f"{source}->{target}, key={key}"
        if edge_data.get("length") is None:
            raise ValueError(f"Graph contains edge without length after normalization ({edge_label}).")

        raw_length = edge_data["length"]
        try:
            length_m = float(raw_length)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Edge length is not numeric for edge {edge_label}: {raw_length!r}") from exc

        if length_m <= 0:
            raise ValueError(f"Edge length must be positive for edge {edge_label}, got {length_m}.")
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
        add_edge_lengths = _resolve_add_edge_lengths(ox)
        graph = add_edge_lengths(graph)

    _normalise_edge_distances(graph)
    return graph
