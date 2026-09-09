# Integration record — 2026-09-08

Branch: integration/ppe-unified. Base: main at 70d95d1.
Remote: volethanhtrieu/YOLOv26_PPE_project_team_15.
Remote refs were refreshed before integration.

| Source | Commit | Treatment |
| --- | --- | --- |
| feature/bytetrack | dc4e07e | Merged; review API, jobs, human review, four-class converter, W&B and ablation |
| feature/ppe-association (remote) | 3ed30f0 | Merged; latest Variant C and benchmark |
| feature/event-engine | 3e6b0f4 | Merged independent Git history; backend, configuration, tests |
| feature/training | e981b8b | Merged; reproducible training package and container workflow |
| feature/data-pipeline (local) | c9a362a | Merged; CHVG preparation and noise experiments |
| feature/shel5k-4class | c6aa378 | Included through event-engine ancestry |
| bytetrack / local association / remote backup | e2b47cf | Already included through ByteTrack ancestry |
| sample/phase2-5class | 3fb8fa4 | Historical ancestor; final runtime remains four-class |
| setup/project-structure | 32cde0f | Already in main ancestry |
| Event-Engine | ee57add | Older standalone prototype preserved in archive/event_engine_prototype/; not a supported runtime |

There was no remote feature/ppe-monitoring-production branch in the fetched
remote head list. No unpublished source from a missing branch is claimed here.

## Resolution decisions

- Root README replaced with unified setup/module map, not a branch-switch guide.
- Both colliding association tests retained (test_association.py and
  test_event_association.py).
- Latest research majority-voting configuration retained; stale test expected
  consecutive mode and an older checkpoint filename and was updated.
- Root device defaults to CPU and API host to loopback.
- Review and research event semantics remain separate and documented.
- ppe.py routes commands to correct working directories using sys.executable.
- Ultralytics pinned to the tracker API version used locally.
- Model/video/database/W&B runtime artifacts removed from the new Git tree
  using cached-only removal. Files on disk and source branch history remain.
- Historical prototype preserved, but not mixed into supported runtime imports.
- SQLite current-thread close method added for deterministic Windows cleanup.

## Verification

| Check | Result |
| --- | --- |
| pytest tests | 25 passed |
| ByteTrack ablation unit script | PASS |
| Review API smoke --allow-empty | PASS; evidence/clip checks skipped without a published event |
| Job API smoke --allow-empty | PASS; no completed job preview fixture |
| Human Review V3 smoke | PASS, zero-state |
| Review inference → association → Event Engine | PASS, 3 real video frames, not published |
| Standalone Variant C inference | PASS, 3 real video frames |
| Research Event Engine inference | PASS, 3 real video frames |

Real-model checks used the existing models/PPE-merged-best.pt and video/test2.mp4.
Model reported exactly person/head/helmet/vest. These are external ignored
artifacts and not bundled in a fresh clone.
Tests used the existing local Python environment, not a clean install.
The offline GitHub workflow has been added but has not run remotely.

Smoke runs do not prove recall, ID stability, alert quality, long-video stability,
online W&B upload, or deployment security. No retraining, publish, push or
main merge was performed. A review of complete video output and CI on a clean
runner is still required before release.

## Reproduce the real-model check

```powershell
python ppe.py smoke-inference --model "C:\models\best.pt" --video "C:\videos\test.mp4"
python ppe.py infer --model "C:\models\best.pt" --video "C:\videos\test.mp4" --max-frames 3 --run-name smoke
```

Use a new run name if the output directory already exists.
