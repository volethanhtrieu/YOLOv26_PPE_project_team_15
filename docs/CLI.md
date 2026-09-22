# CLI reference

Run `python ppe.py <command> [arguments]` from the repository root.
The launcher uses the active Python executable and passes arguments unchanged.
Paths supplied by the user should be absolute, except root config.yaml for the
research commands. There is no single global configuration file for all runtimes.

| Command | Target directory | Role |
| --- | --- | --- |
| review-api | bytetrack_ppe | Local Flask review API; port 5000 |
| dashboard | bytetrack_ppe | Streamlit review UI |
| infer | bytetrack_ppe | Isolated detection/tracking/event run |
| wandb | bytetrack_ppe | Optional W&B inference workflow |
| ablation | bytetrack_ppe | Evaluate ablation outputs |
| event-api | repository root | Research Flask API |
| event-video | repository root | Research video processing and A–D profiles |
| check-model | repository root | Inspect configured model classes |
| association | repository root | Standalone Variant C video processing |
| convert | repository root | Convert CHVG labels to four classes |
| validate | repository root | Compare converted dataset with source |
| train | repository root | CHVG4 baseline-training script |
| test | repository root | Offline tests under tests/ |
| smoke-inference | repository root | Short real-model test of Variant C and research runtime |

For argument-based commands, append --help to see the exact installed command
interface. review-api is a development-server script, not an argument parser;
do not run it with --help expecting it to exit.

## Configuration ownership

| Workflow | Configuration owner | Checkpoint |
| --- | --- | --- |
| Review inference | infer arguments + bytetrack_ppe/configs/bytetrack_ppe.yaml | --model; default bytetrack_ppe/weights/candidates/CHVG4-best.pt |
| Research | root config.yaml | model.path; default weights/best.pt |
| Variant C | association arguments + implementation settings | --model |
| CHVG4 training | train arguments | --model (pretrained starting model) |
| Final training | experiments/training/configs/training.yaml | Separate package/environment |

Changing config.yaml does not change the review pipeline. Changing review
tracker settings does not configure Variant C's use of the library tracker.
Existing confidence thresholds are operating settings, not proven optima.

## Safe local inference

```powershell
python ppe.py infer --video "C:\videos\site.mp4" --model "C:\models\ppe.pt" --max-frames 30 --device cpu --run-name site-smoke-01
```

Use a fresh run name. --publish changes the review application's published
dataset and is deliberately absent above. Do not publish tracking-off ablations.

## Research workflow

Set model.path in root config.yaml, then:

```powershell
python ppe.py check-model --config config.yaml
python ppe.py event-video --config config.yaml --source "C:\videos\site.mp4" --profile D_full_system
```

Profile A/B/C/D definitions belong to this runtime. Neither these profiles nor
its API payloads should be assumed identical to the review application.

## API boundaries

| Surface | Review application | Research runtime |
| --- | --- | --- |
| Health | /api/health (published-store readiness) | /health (worker status) |
| Video processing | Job and preview workflow | /api/start, /api/stop, /video_feed |
| Events | Published event log and human review | Research SQLite event log |
| Startup needs | Can start without model/published data | Loads the configured model |

Do not run both on port 5000. Use module-specific documentation for endpoint
payloads; sharing an /api/events path does not mean sharing a contract.
