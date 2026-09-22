# Troubleshooting

| Symptom | Check | Action |
| --- | --- | --- |
| config.yaml or check_model.py not found | Current directory and branch | Use repository root on main_sub; run ppe.py |
| Import selects the wrong app.py | Review vs research runtime | Use review-api or event-api; do not combine module paths manually |
| Python/package versions differ | python --version; python -m pip --version | Activate the same environment in each terminal |
| CUDA unavailable | Installed PyTorch build and device | Use CPU first; configure GPU explicitly in the selected runtime |
| Model file not found | Model path for the chosen runtime | Supply a trusted checkpoint; weights are not bundled |
| Class mismatch | Printed model.names | Verify IDs 0–3 are person/head/helmet/vest; changing YAML does not retrain a model |
| Review health returns 503 | Published store exists? | Empty store is expected before publish; partially missing data needs investigation |
| Dashboard has no new events | Is the run only a preview? | Publish deliberately after checking the isolated result |
| Port 5000 already in use | Another API process | Stop the other server; review and research defaults use the same port |
| W&B shows a bar instead of a curve | Summary versus per-frame history | Select a history metric; not every logged field is a time series |
| Many unique tracks | Missed detections, occlusion, fragmented IDs | Inspect the annotated video; unique ID count is not a person-count ground truth |

## Model inspection is not equally strict in all runtimes

The review pipeline and Variant C enforce the canonical class order. The research
check-model command currently compares the set of class names, and its detector
adapter warns on missing names. Therefore a successful check-model message alone
does not prove the checkpoint's ID order. Inspect the printed mapping explicitly.

## Report a reproducible issue

Include the branch/commit, runtime, command, relevant configuration, package
versions and traceback. Use a small redistributable sample when possible.
Remove API keys, signed links, private filesystem paths and confidential footage.
See the issue templates and [contributing guide](../CONTRIBUTING.md).
