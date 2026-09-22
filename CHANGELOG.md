# Changelog

This file records repository changes, not model benchmark results.

## Unreleased — main_sub

### Documentation and maintenance

- Rebuilt the project overview with pipeline, workflow selection and outputs.
- Added English/Vietnamese onboarding, CLI, troubleshooting and testing guides.
- Distinguished final training, baseline training and historical data workflows.
- Added contribution guidance, issue/PR templates and safe-operation notes.
- Added local documentation-link checks and empty-state API checks to CI.

### Integration baseline — 2026-09-08

- Integrated data preparation, training, ByteTrack, Association and Event Engine.
- Added the shared ppe.py launcher while retaining runtime boundaries.
- Removed generated artifacts from the tracked tree without rewriting history.
- Recorded 25 local regression tests and short real-model smoke tests.

See [the integration record](docs/INTEGRATION.md) for source commits and test scope.
No published release version or production-readiness claim is implied.
