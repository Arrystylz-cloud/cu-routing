"""Campus graph construction utilities."""

from __future__ import annotations

import networkx as nx


def build_walking_graph_from_polygon(_polygon_geojson_path: str) -> nx.MultiDiGraph:
    """Return a placeholder graph.

    TODO(issue): Replace placeholder with OSMnx implementation.
    """
    graph = nx.MultiDiGraph()
    return graph
