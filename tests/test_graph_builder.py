from __future__ import annotations

import json

import networkx as nx
import pytest

from src import graph_builder


def _write_boundary(path) -> None:
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [3.146, 6.669],
                            [3.161, 6.669],
                            [3.161, 6.678],
                            [3.146, 6.678],
                            [3.146, 6.669],
                        ]
                    ],
                },
                "properties": {},
            }
        ],
    }
    path.write_text(json.dumps(feature_collection), encoding="utf-8")


class _FakePolygon:
    geom_type = "Polygon"
    is_empty = False


class _FakeMultiPolygon:
    geoms = ()


def _patch_shapely(monkeypatch) -> None:
    monkeypatch.setattr(
        graph_builder,
        "_import_shapely_geometry",
        lambda: (_FakeMultiPolygon, _FakePolygon, lambda _: _FakePolygon()),
    )


class _FakeDistanceModule:
    def __init__(self, length_to_fill: float = 42.0) -> None:
        self.length_to_fill = length_to_fill
        self.called = False

    def add_edge_lengths(self, graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
        self.called = True
        for _, _, _, edge_data in graph.edges(keys=True, data=True):
            edge_data.setdefault("length", self.length_to_fill)
        return graph


class _FakeOsmnx:
    def __init__(self, graph: nx.MultiDiGraph) -> None:
        self._graph = graph
        self.distance = _FakeDistanceModule()
        self.received_polygon = None
        self.received_kwargs = {}

    def graph_from_polygon(self, polygon, *, network_type: str, simplify: bool) -> nx.MultiDiGraph:
        self.received_polygon = polygon
        self.received_kwargs = {"network_type": network_type, "simplify": simplify}
        return self._graph


def test_build_walking_graph_loads_walk_network_and_sets_distance_m(tmp_path, monkeypatch):
    boundary_path = tmp_path / "campus_boundary.geojson"
    _write_boundary(boundary_path)

    _patch_shapely(monkeypatch)
    graph = nx.MultiDiGraph()
    graph.add_edge(1, 2, key=0, length=15.5)
    fake_osmnx = _FakeOsmnx(graph)
    monkeypatch.setattr(graph_builder, "_import_osmnx", lambda: fake_osmnx)

    result = graph_builder.build_walking_graph_from_polygon(str(boundary_path))

    assert isinstance(result, nx.MultiDiGraph)
    assert fake_osmnx.received_kwargs == {"network_type": "walk", "simplify": True}
    assert fake_osmnx.received_polygon.geom_type == "Polygon"
    assert result.edges[1, 2, 0]["distance_m"] == pytest.approx(15.5)
    assert fake_osmnx.distance.called is False


def test_build_walking_graph_adds_missing_length_before_distance_m(tmp_path, monkeypatch):
    boundary_path = tmp_path / "campus_boundary.geojson"
    _write_boundary(boundary_path)

    _patch_shapely(monkeypatch)
    graph = nx.MultiDiGraph()
    graph.add_edge(1, 2, key=0)
    fake_osmnx = _FakeOsmnx(graph)
    monkeypatch.setattr(graph_builder, "_import_osmnx", lambda: fake_osmnx)

    result = graph_builder.build_walking_graph_from_polygon(str(boundary_path))

    assert fake_osmnx.distance.called is True
    assert result.edges[1, 2, 0]["distance_m"] == pytest.approx(42.0)


def test_build_walking_graph_rejects_invalid_geojson(tmp_path):
    invalid_boundary_path = tmp_path / "campus_boundary.geojson"
    invalid_boundary_path.write_text(json.dumps({"type": "FeatureCollection", "features": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="No polygon geometry"):
        graph_builder.build_walking_graph_from_polygon(str(invalid_boundary_path))
