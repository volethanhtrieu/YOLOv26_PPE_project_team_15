# Documentation

Start with the root [README](../README.md), then choose the task you need.
Commands in the new guides use the repository root and the shared ppe.py launcher.

| Guide | Purpose |
| --- | --- |
| [Quick start](QUICKSTART.md) / [Tiếng Việt](QUICKSTART_VI.md) | Install and run locally |
| [Architecture](architecture.md) | Understand pipeline and runtime boundaries |
| [CLI reference](CLI.md) | Choose commands, paths and configuration |
| [Testing](TESTING.md) | Test tiers and release checks |
| [Troubleshooting](TROUBLESHOOTING.md) | Environment, paths, readiness and model issues |
| [Training workflows](TRAINING_PATHS.md) | Choose CHVG baseline or final-training package |
| [Data](../data/README.md) | Dataset versions and class contract |
| [Integration record](INTEGRATION.md) | Historical branch provenance and 08 September results |

## Module references

These documents retain module-specific details and historical experiments.
Their commands may assume a module directory or environment; read the notice
at the top before running them.

- [Review application](../bytetrack_ppe/README.md)
- [Standalone Association](../README_VARIANT_C.md)
- [Research Event Engine](EVENT_ENGINE.md)
- [CHVG five-class preparation and noise experiments](../README_CHVG.md)
- [CHVG four-class training](../TRAINING_GUIDE_CHVG4.md)
- [Final-training package](../experiments/training/INSTALL.md)
- [Historical Event Engine prototype](../archive/event_engine_prototype/README.md)

The current branch combines implementations; it does not turn distinct research
policies into one common event definition. Do not mix their metrics.
