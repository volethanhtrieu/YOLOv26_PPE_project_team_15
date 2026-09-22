# Training workflows

There are two workflows because the project evolved from CHVG experiments to
a consolidated final-training package. They are not aliases.

| | CHVG4 baseline | Final-training package |
| --- | --- | --- |
| Entry | python ppe.py train | experiments/training/src/train_yolo26l.py |
| Guide | [CHVG4 guide](../TRAINING_GUIDE_CHVG4.md) | [Installation](../experiments/training/INSTALL.md) |
| Configuration | CLI arguments | experiments/training/configs/training.yaml |
| Starting defaults | yolov8l.pt, image size 640, 100 epochs | Consult the package configuration and model card |
| Environment | Root environment | Separate pinned training environment/container |
| Purpose | Validated CHVG4 experiments | Reproduce the final documented YOLO26L training workflow |

Do not run ppe.py train and describe its defaults as the final YOLO26L recipe.
Do not install the training CUDA requirements blindly into an inference
environment. Read each workflow's working-directory assumptions.

## Before training

1. Confirm data provenance and redistribution rights.
2. Validate the dataset and class order: person, head, helmet, vest.
3. Record the dataset manifest/version and train/validation/test policy.
4. Record the starting checkpoint and environment.
5. Keep test data out of training and epoch validation.

## Handoff to inference

Provide checkpoint hash, class order, dataset version, input size, training
configuration, evaluation split and metrics. Include a W&B link only if sharing
is intended. Do not rely on the name best.pt to identify a model.

The existing [model card](../experiments/training/docs/MODEL_CARD.md) records
missing final artifacts. Do not replace missing results with numbers from a
different run or a slide.
