# Research Event Engine

This guide covers the root backend/ implementation and A–D research profiles.
It is separate from the review application in bytetrack_ppe/.
Use the [root environment](QUICKSTART.md) and run commands from the repository
root. [Runtime comparison](architecture.md).

## Pipeline and data contract

Video → YOLO detections/tracks → head/torso ROI association → temporal voting →
SQLite events, evidence and CSV logs.

The current project schema is **0 person, 1 head, 2 helmet, 3 vest**.
Earlier three-class experiments are not the setup for this branch. Do not remove
vest from config.yaml merely to make an old model pass.

The detector adapter currently sends all detection classes through YOLO.track.
This differs from the person-only tracking used by the review/Variant C runtimes.
Event outputs use research status values such as active/resolved, not the
review application's human-decision workflow.

## Prepare the checkpoint

Weights and test videos are external artifacts. Supply a trusted model at
weights/best.pt or edit model.path in root config.yaml to an absolute path.

```powershell
python ppe.py check-model --config config.yaml
```

Inspect the printed mapping explicitly. The current research checker compares
class names as a set; it does not enforce their numeric order. The review and
Variant C runtimes apply stricter schema checks.

## Current configuration

The authoritative file is [config.yaml](../config.yaml).

| Setting | Committed default | Role |
| --- | --- | --- |
| model.imgsz | 640 | Inference input size |
| model.confidence | 0.25 | Detection threshold |
| model.iou | 0.50 | Detection overlap threshold |
| model.device | cpu | Explicit device |
| tracking.tracker | bytetrack.yaml | Library tracker configuration |
| tracking.missing_timeout_seconds | 3.0 | Missing-track event timeout |
| event.mode | majority | Temporal voting policy |
| event.violation_seconds | 2.0 | Required violation duration |
| event.recovery_seconds | 1.0 | Recovery duration |
| event.voting_window_seconds | 2.5 | Voting window |
| event.voting_ratio | 0.70 | Voting ratio |
| event.min_voting_samples | 5 | Minimum samples |

The event duration is not a promise that every event appears exactly two seconds
after a worker enters the scene: observations and voting conditions also matter.
These are operating settings, not claimed optimal parameters.
Set device to "0" only with a compatible GPU environment.

## Run a video

Replace the example source path. Choose output/log names and a camera ID that
identify the experiment:

```powershell
python ppe.py event-video --config config.yaml --source "C:\videos\site.mp4" --output outputs/site-D.mp4 --log-output logs/site-D.csv --camera-id site-D --profile D_full_system
```

Inspect the annotated video and CSV after completion. This runtime does not
create review-dashboard jobs or publish into the review store.
Reusing an output path may overwrite that artifact; use a new name per run.
Database history persists at the configured storage.database path.

| Artifact | Default location |
| --- | --- |
| Annotated video | outputs/annotated.mp4 unless --output is supplied |
| Per-run violation log | logs/ unless --log-output is supplied |
| Evidence images | evidence/ |
| Research event history | data/detections.db |

Events include camera_id, track_id, violation_type, status, timestamps,
confidence and evidence_path. They are generated candidates, not automatically
verified safety violations.

## A–D profiles

| Profile | Tracking | ROI association | Event Engine |
| --- | --- | --- | --- |
| A_yolo | Off | Off | Off |
| B_tracking | On | Off | Off |
| C_association | On | On | Off |
| D_full_system | On | On | On |

Use --profile to select one. A–C disable Event Engine and therefore do not
provide the same event output as D. Do not compare alert counts without
accounting for the enabled modules.
For comparisons, hold video, checkpoint and other relevant settings fixed.
Record metric definitions and ground-truth availability.

## Local API

```powershell
python ppe.py event-api --config config.yaml --profile D_full_system
```

The configured model is loaded at startup. Default address:
http://127.0.0.1:5000. Stop the review API first if it is using the same port.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /health | Worker status |
| GET | /api/config | Effective runtime configuration |
| POST | /api/start | Start a video/camera worker |
| POST | /api/stop | Stop the worker |
| GET | /video_feed | MJPEG output |
| GET | /api/stats | Worker and pipeline statistics |
| GET | /api/events | Research events |
| GET | /api/events.csv | Export event history |
| GET | /api/evidence/<filename> | Retrieve evidence |

For POST /api/start, supply JSON with source and camera_id. See
[app.py](../app.py) for accepted input and response details.
This is a trusted-local API, not a public deployment.

## Optional W&B logging

Authenticate only when an online run is intended. Do not put keys in commands,
commits or issue reports. After wandb login:

```powershell
python ppe.py event-video --config config.yaml --source "C:\videos\site.mp4" --output outputs/site-wb.mp4 --camera-id site-wb --profile D_full_system --wandb --wandb-project ppe-ablation --wandb-run-name site-D --wandb-log-every 1
```

Add --wandb-no-video to avoid the annotated-video upload in this workflow.
Ensure any uploaded footage and metadata may be shared. Inference metrics
describe speed/output behaviour; they do not establish event accuracy.

## Verification

Run python ppe.py test -q for offline tests. Use the
[test guide](TESTING.md) for model smoke tests and evaluation boundaries.
For failures, check [troubleshooting](TROUBLESHOOTING.md) before changing the
model schema or removing dependencies.
