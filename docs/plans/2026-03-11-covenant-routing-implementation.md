# Covenant University Routing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a reproducible Python pipeline that collects campus building coordinates, computes shortest routes, and exports validated CSV outputs.

**Architecture:** A modular data pipeline with four stages: collection, graph construction, routing, and export. OSMnx provides the campus path network, NetworkX computes shortest paths, and CSV artifacts are generated with schema checks for reproducibility.

**Tech Stack:** Python 3.11+, pandas, osmnx, networkx, geopandas, shapely, pytest

---

## Confirmed Scope
- Travel mode: `walking` only.
- Route generation: `all building pairs`.
- Primary source data: `OpenStreetMap` for building coordinates and walk network.
- Accuracy target: soft threshold of `95%` building coverage, with manual overrides for missing buildings.
- Workflow note: do not initialize a Git repository and do not create commits for this work.

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `src/data_collection.py`
- Create: `src/graph_builder.py`
- Create: `src/router.py`
- Create: `src/export_csv.py`
- Create: `src/config.py`
- Create: `tests/test_smoke.py`

**Step 1: Write the failing smoke test**

```python
def test_modules_import():
    import src.data_collection
    import src.graph_builder
    import src.router
    import src.export_csv
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_smoke.py -v`
Expected: FAIL due to missing modules.

**Step 3: Write minimal implementation**

Create empty module files with minimal import-safe content.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_smoke.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_smoke.py -v`
Expected: PASS and modules import cleanly.

### Task 2: Building Coordinate Ingestion

**Files:**
- Create: `data/manual/buildings_seed.csv`
- Modify: `src/data_collection.py`
- Create: `tests/test_data_collection.py`

**Step 1: Write the failing test**

```python
def test_load_buildings_has_required_columns(tmp_path):
    # build small CSV fixture and assert required schema
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_collection.py -v`
Expected: FAIL because loader is not implemented.

**Step 3: Write minimal implementation**

Implement:
- CSV loader,
- required-column validation,
- stable `building_id` generation,
- null/duplicate checks.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_collection.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_data_collection.py -v`
Expected: PASS with schema checks green.

### Task 3: Campus Graph Construction

**Files:**
- Modify: `src/graph_builder.py`
- Create: `tests/test_graph_builder.py`
- Create: `data/manual/campus_boundary.geojson`

**Step 1: Write the failing test**

```python
def test_graph_has_positive_edge_lengths():
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_graph_builder.py -v`
Expected: FAIL because graph builder is incomplete.

**Step 3: Write minimal implementation**

Implement:
- OSMnx graph download by boundary,
- graph simplification,
- edge length normalization to `distance_m`,
- optional local cache support.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_graph_builder.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_graph_builder.py -v`
Expected: PASS with positive edge lengths.

### Task 4: Map Buildings to Network Nodes

**Files:**
- Modify: `src/router.py`
- Create: `tests/test_node_mapping.py`

**Step 1: Write the failing test**

```python
def test_building_to_node_mapping_returns_node_id():
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_node_mapping.py -v`
Expected: FAIL due to missing mapping function.

**Step 3: Write minimal implementation**

Implement nearest-node mapping with:
- coordinate validation,
- error on out-of-bound points,
- deterministic output.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_node_mapping.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_node_mapping.py -v`
Expected: PASS with deterministic node mapping.

### Task 5: Shortest Path Computation

**Files:**
- Modify: `src/router.py`
- Create: `tests/test_router.py`

**Step 1: Write the failing test**

```python
def test_shortest_path_returns_distance_and_nodes():
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_router.py -v`
Expected: FAIL due to missing shortest path logic.

**Step 3: Write minimal implementation**

Implement:
- `find_shortest_path(origin_id, destination_id, algorithm="dijkstra")`,
- total distance calculation,
- estimated time using configurable walking speed,
- graceful error for disconnected nodes.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_router.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_router.py -v`
Expected: PASS with valid shortest-path outputs.

### Task 6: CSV Export Layer

**Files:**
- Modify: `src/export_csv.py`
- Create: `tests/test_export_csv.py`

**Step 1: Write the failing test**

```python
def test_route_export_contains_required_columns(tmp_path):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_export_csv.py -v`
Expected: FAIL because exporter is incomplete.

**Step 3: Write minimal implementation**

Implement CSV writers for:
- `buildings.csv`,
- `graph_edges.csv`,
- `routes.csv`,
- summary validation report.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_export_csv.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_export_csv.py -v`
Expected: PASS with required CSV columns present.

### Task 7: Pipeline Orchestration CLI

**Files:**
- Create: `main.py`
- Modify: `src/config.py`
- Create: `tests/test_main_cli.py`

**Step 1: Write the failing test**

```python
def test_cli_runs_pipeline_and_writes_outputs(tmp_path):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_main_cli.py -v`
Expected: FAIL due to missing CLI pipeline.

**Step 3: Write minimal implementation**

Implement CLI flow:
- load config,
- ingest coordinates,
- build graph,
- compute selected routes,
- export CSV results.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_main_cli.py -v`
Expected: PASS.

**Step 5: Verification checkpoint**

Run: `pytest tests/test_main_cli.py -v`
Expected: PASS and CLI pipeline writes expected outputs.

### Task 8: End-to-End Validation and Docs

**Files:**
- Create: `README.md`
- Create: `docs/output-schema.md`
- Modify: `tests/test_smoke.py`

**Step 1: Write the failing integration check**

```python
def test_end_to_end_generates_all_expected_csv(tmp_path):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_smoke.py -v`
Expected: FAIL until integration wiring is complete.

**Step 3: Write minimal implementation**

Add integration hooks and output docs:
- run instructions,
- configuration examples,
- schema details and sample rows.

**Step 4: Run test suite**

Run: `pytest -v`
Expected: all tests PASS.

**Step 5: Verification checkpoint**

Run: `pytest -v`
Expected: all tests PASS.

## Final Verification Checklist
- Run: `pytest -v`
- Run: `python main.py --help`
- Run: `python main.py --origin <id> --destination <id> --output-dir data/processed`
- Confirm output files:
  - `data/processed/buildings.csv`
  - `data/processed/graph_edges.csv`
  - `data/processed/routes.csv`
- Spot-check at least 5 routes for plausibility.

## Open Decisions (Need User Confirmation)
- None currently. Proceed with confirmed scope and defaults.
