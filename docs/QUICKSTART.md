# Run the unified repository

Start in the repository root. For a new environment use Python 3.11 or 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python ppe.py test -q
```

Ultralytics is pinned to 8.4.104 because tracker APIs are version-sensitive.
Choose PyTorch appropriate for your hardware. The training package has its own
CUDA requirements; do not blindly combine them with a local inference environment.

## Review application

```powershell
python ppe.py review-api
```

In a second terminal with the same environment:

```powershell
python ppe.py dashboard
```

Open http://localhost:8501 and use API URL http://127.0.0.1:5000.
Create a video job, inspect the isolated preview, publish deliberately, then use
Review Queue / Events. Human decisions remain separate from AI status.
Outputs are under bytetrack_ppe/outputs/.
These development servers are for trusted local use, not public deployment.

## Video inference

Use absolute paths for inputs: the launcher changes directory for each module.

```powershell
python ppe.py infer --help
python ppe.py infer --video "C:\videos\test.mp4" --model "C:\models\best.pt" --device cpu
python ppe.py wandb --help
```

Review defaults: detection confidence 0.10, PPE association 0.20, tiles 1×1.
Tracker config: bytetrack_ppe/configs/bytetrack_ppe.yaml.
These are inherited operating settings, not claimed optimal thresholds.
W&B is optional; only upload videos when sharing is permitted.

## Research Event Engine and Association

Edit model.path in config.yaml to a trusted four-class checkpoint.
Device defaults to CPU; choose GPU explicitly when available.

```powershell
python ppe.py check-model --config config.yaml
python ppe.py event-video --source "C:\videos\test.mp4" --config config.yaml --profile D_full_system
python ppe.py association --model "C:\models\best.pt" --source "C:\videos\test.mp4" --device cpu
```

Research output: outputs/annotated.mp4, logs/ CSV, evidence/ images and
data/detections.db. Association output: outputs/variant_c.mp4 and variant_c.jsonl.
Do not run event-api and review-api simultaneously on port 5000.

## Data and training

```powershell
python ppe.py convert --source-yaml "C:\datasets\chvg8\data.yaml" --output "C:\datasets\chvg4"
python ppe.py validate --source-yaml "C:\datasets\chvg8\data.yaml" --target-yaml "C:\datasets\chvg4\data_4class.yaml" --report-dir "C:\datasets\chvg4\validation"
python ppe.py train --help
```

Conversion creates a new dataset and preserves splits/coordinates; glass is
dropped. Train only after validation passes.
For the final reproducible training package use experiments/training/INSTALL.md;
its commands are relative to experiments/training, not the repository root.
See README_CHVG.md for noise experiments.

## Tests

```powershell
python ppe.py test -q
python bytetrack_ppe/test_ablation_v1.py
python bytetrack_ppe/test_api.py --allow-empty
python bytetrack_ppe/test_job_api_v3.py --allow-empty
python bytetrack_ppe/test_human_review_v3.py
```

The API scripts use Flask test clients; no live server is needed.
An empty checkout only tests empty-state endpoints. Evidence and clip assertions
require a completed published run. Unit tests do not run real-model inference.
Without published data, /api/health intentionally returns 503 (not ready).
The --allow-empty flag accepts only a completely missing published store;
partial data still fails. Omit the flag when checking a published deployment.
Check Python environment, current directory and input paths if commands fail.
Do not paste escaped underscores in filenames.
