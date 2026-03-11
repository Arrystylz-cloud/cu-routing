# Covenant University Routing Project TODO

## Understanding
- [x] Confirm project objective: collect building coordinates, compute shortest paths, and export CSV outputs.
- [x] Identify major ambiguities and dependencies.

## Plan
- [x] Draft design options and select recommended architecture.
- [x] Draft implementation plan with phased milestones and verification steps.
- [ ] Confirm remaining open decisions with stakeholder.

## Execution Phases
- [ ] Phase 1: Environment setup and dependency installation.
- [ ] Phase 2: Building coordinate ingestion and validation.
- [ ] Phase 3: Campus graph extraction and edge weighting.
- [ ] Phase 4: Building-to-node mapping.
- [ ] Phase 5: Shortest path computation.
- [ ] Phase 6: CSV export and schema checks.
- [ ] Phase 7: End-to-end tests and documentation.

## Deliverables
- [ ] `data/processed/buildings.csv`
- [ ] `data/processed/graph_edges.csv`
- [ ] `data/processed/routes.csv`
- [ ] Validation summary report

## Open Questions
- [x] First release travel mode: walking only.
- [x] Routing output scope: all building pairs.
- [x] Primary source of truth: OpenStreetMap.
- [x] Acceptance target for v1: soft target of 95% building coverage with manual overrides for gaps.

## Review
- Design document: `docs/plans/2026-03-11-covenant-routing-design.md`
- Implementation plan: `docs/plans/2026-03-11-covenant-routing-implementation.md`
- Current status: planning decisions finalized; ready for implementation.
