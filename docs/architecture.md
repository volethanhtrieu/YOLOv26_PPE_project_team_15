# Architecture

This branch unifies delivery, not independent experiment semantics.

| Runtime | Entry | Role |
| --- | --- | --- |
| Review | ppe.py infer/review-api/dashboard | Person tracking, PPE association, isolated jobs, evidence, publish, human review |
| Variant C | ppe.py association | Track person and detect PPE separately, then associate |
| Research | ppe.py event-video/event-api | Existing detector adapter, ROI association, temporal voting, SQLite, A–D profiles |

Review flow: video → YOLO → person ByteTrack → PPE association → temporal
events → preview → explicit publish → human review.
Track output includes ID, box and detection confidence. Confidence is not an
identity accuracy probability.

The research adapter tracks all detection classes through YOLO.track;
Variant C and review track person only. This difference is preserved.
Review missing-vest evidence is suspected; research uses its own voting rules.
Do not compare event totals as if these policies were identical.

Root config.yaml controls the research runtime only. Review CLI arguments and
bytetrack_ppe/configs/bytetrack_ppe.yaml control the review runtime.
Historical data scripts/reports can describe earlier schemas; final inference
uses person/head/helmet/vest.

Future consolidation into one semantic runtime requires explicit shared
person/PPE/event contracts and regression tests. Both implementations are
retained here to avoid removing existing functionality.
