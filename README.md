# PPE Monitoring — Team 15

Four-class PPE detection, tracking, association, temporal events, evidence and
human review. Data preparation, training and benchmarking are available in
one branch: no branch switching is required.

**Final schema:** 0 person · 1 head · 2 helmet · 3 vest.
The checkpoint must match this class order.

## Start here

- [Installation, commands and tests](docs/QUICKSTART.md)
- [Runtime architecture](docs/architecture.md)
- [Integration provenance and verification](docs/INTEGRATION.md)
- [Review application](bytetrack_ppe/README.md)
- [Association benchmark](README_VARIANT_C.md)
- [Research Event Engine](docs/EVENT_ENGINE.md)
- [Data preparation](README_CHVG.md)
- [CHVG4 training](TRAINING_GUIDE_CHVG4.md)
- [Reproducible final-training environment](experiments/training/INSTALL.md)

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python ppe.py test -q
python ppe.py --help
python ppe.py review-api
```

In a second activated terminal: `python ppe.py dashboard`.
API: http://127.0.0.1:5000. Dashboard: http://localhost:8501.
Supply trusted four-class weights before inference. Training and W&B login
are not required for local inference or the review API.

## Layout

| Location | Responsibility |
| --- | --- |
| ppe.py | Common launcher using the active Python environment |
| bytetrack_ppe/ | Video jobs, person tracking, evidence, publish, human review |
| src/variant_c/ | Standalone person-to-PPE association |
| backend/ | Research Event Engine, SQLite and A–D profiles |
| scripts/data/, configs/ | Data preparation, conversion and validation |
| scripts/train/, experiments/training/ | Training workflows |
| tests/, docs/ | Regression tests and documentation |

The review and research runtimes retain different event policies and storage.
They are not interchangeable APIs; see the architecture note.
Generated videos, weights, databases and W&B logs are ignored.
Historical reports are not guarantees of current model quality.

Offline tests do not establish model accuracy or production readiness.
Use local servers on trusted machines only. See [contributing](CONTRIBUTING.md).
