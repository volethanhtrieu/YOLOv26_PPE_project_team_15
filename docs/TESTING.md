# Testing and verification

Tests answer different questions. A passing API check is not a measurement of
tracking accuracy; a short inference run is not a long-video reliability test.

## Test tiers

| Tier | Command | Requires external assets? | What it checks |
| --- | --- | --- | --- |
| Documentation | python scripts/check_docs.py | No | Local links in maintained guides |
| Regression | python ppe.py test -q | No | Data conversion, backend, association and launcher contracts |
| Ablation units | python bytetrack_ppe/test_ablation_v1.py | No | Replay and frame-local identity helpers |
| Empty API | Commands below | No | Endpoint/zero-state behaviour, not event media |
| Real-model smoke | python ppe.py smoke-inference --model … --video … | Model and video | Small inference sample in two standalone runtimes |
| Review pipeline | python ppe.py infer --model … --video … --max-frames 30 | Model and video | Tracking/event artifact generation |
| Published media | API smoke without --allow-empty | Published completed run | Available event/evidence/clip endpoints |
| Quality evaluation | Separate annotated test set | Ground truth | Detection, tracking and event quality |

### Offline suite

```sh
python scripts/check_docs.py
python ppe.py test -q
python bytetrack_ppe/test_ablation_v1.py
python bytetrack_ppe/test_api.py --allow-empty
python bytetrack_ppe/test_job_api_v3.py --allow-empty
python bytetrack_ppe/test_human_review_v3.py
```

API scripts use Flask test clients; no live server is required.
--allow-empty accepts a completely absent published store, not a partly missing
store. A fresh checkout reports 503 at /api/health by design.
For published data, omit the flag and read the log: assertions requiring an
event or completed job can be skipped if no suitable fixture exists.

### Real-model smoke

```powershell
python ppe.py smoke-inference --model "C:\models\ppe.pt" --video "C:\videos\site.mp4" --frames 3
python ppe.py infer --model "C:\models\ppe.pt" --video "C:\videos\site.mp4" --max-frames 30 --run-name smoke-01
```

Use a fresh run name; do not publish smoke output by default.
The first command tests Variant C and the research runtime. The second tests
the review detection/tracking/event workflow.

## CI coverage

The offline workflow installs dependencies and runs the regression, ablation,
documentation and empty-state API checks. It does not download private weights,
train a model, upload W&B media, or evaluate ground-truth accuracy.
Check the actual Actions run after pushing; the presence of a workflow file is
not evidence that a clean install or all platforms pass.

The existing training-image workflow is separate. Its publication behaviour is
unchanged: this documentation update does not deploy a service or publish an image.

## Before release

- [ ] Clean-environment installation and CI pass on the intended platform.
- [ ] Run a representative full-length video; inspect ID continuity and output length.
- [ ] Verify isolated preview, explicit publish, event media and review history.
- [ ] Record checkpoint hash, class order, dataset/video version and configuration.
- [ ] Test missing files, invalid labels, unavailable devices and interrupted jobs.
- [ ] Validate event quality with annotated cases, including occlusion.
- [ ] Review licensing, artifact sharing and deployment access controls.

The [08 September integration record](INTEGRATION.md) records 25 local tests and
three-frame inference checks. Preserve it as a dated record, not a live status badge.

## Documentation update verification — 2026-09-22

| Local check | Result |
| --- | --- |
| Maintained documentation links | PASS, 20 guides |
| Regression suite | 31 passed (includes six documentation-checker tests) |
| Ablation unit script | PASS |
| Review API, Job API, Human Review V3 | PASS on an empty published store |
| Lint for the new documentation checker/tests | PASS |

Checks used the existing local Python environment. Event media checks were
skipped without a published event. No new model benchmark, full-video run,
clean-environment install or remote Actions run was performed for this
documentation update.
