# Data preparation and versions

Dataset images and annotations are external inputs, not distributed in this
repository. Source code, validation reports and manifests document preparation.

## Canonical inference schema

| ID | Class | Annotation meaning |
| ---: | --- | --- |
| 0 | person | Person/worker |
| 1 | head | Visible bare or unhelmeted head |
| 2 | helmet | Helmet/hard hat |
| 3 | vest | Safety/high-visibility vest |

## Stages

| Stage | Purpose | Reference |
| --- | --- | --- |
| CHVG5 preparation | Inspect source data, merge helmet colours, create initial splits; retain glass | [Historical preparation guide](../README_CHVG.md) |
| CHVG4 conversion | Create a new four-class dataset; remove glass; preserve source images/splits/coordinates | [Conversion report](../reports/dataset/chvg4_conversion_report.md) |
| Final merged dataset | Combine adjudicated sources using the final manifest | [Dataset card](../experiments/training/docs/DATASET_CARD.md) |

CHVG4 conversion reports 1,698 images with a 1,358/170/170 split.
The final merged dataset card reports 4,844 images with a 3,874/484/486 split,
from CHVG4, SHEL4, SH17 and Pictor. Its CHVG component uses the later manifest
split 1,358/169/171. These are different dataset stages, not interchangeable
statistics. Use the manifest for the exact training run.

The final model card has outstanding artifact/metric fields. Dataset validation
PASS is not a model-accuracy result.

## Conversion and validation

Run from repository root with absolute paths:

```powershell
python ppe.py convert --source-yaml "C:\datasets\chvg8\data.yaml" --output "C:\datasets\chvg4"
python ppe.py validate --source-yaml "C:\datasets\chvg8\data.yaml" --target-yaml "C:\datasets\chvg4\data_4class.yaml" --report-dir "C:\datasets\chvg4\validation"
```

The source must have valid available splits. Do not fabricate a val/test split
because a YAML references files that are absent.

Original CHVG mapping:

- blue, red, white, yellow → helmet.
- glass → remove the annotation row.
- head, person, vest → reindex to the canonical IDs.

Validation compares source and target image identities, class counts, label
syntax, bbox coordinate tokens and split membership. The source dataset is not
overwritten. The CHVG baseline trainer requires a passing conversion report;
the final-training package has its own validation workflow.

## Storage and handoff

Use data/raw/, data/interim/, data/processed/ and data/quarantine/ for local data.
Keep generated images/labels and dataset archives outside version control.
Provide source/version, manifest, class mapping, split policy, checksums and
validation output when handing data to another member.

Review source licenses and annotation semantics before reusing or redistributing
data. The [final dataset card](../experiments/training/docs/DATASET_CARD.md)
and [source notes](../experiments/training/docs/THIRD_PARTY_DATASETS.md) describe
provenance. A project software license does not substitute for dataset terms.
