"""Small real-model check of both standalone runtimes; no publish or W&B."""
import argparse
import tempfile
from pathlib import Path

import cv2

from backend.config import load_config
from backend.pipeline import PPEPipeline
from src.variant_c.pipeline import VariantCBackend


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=3)
    args = parser.parse_args()
    if args.frames < 1:
        parser.error("--frames must be positive")
    capture = cv2.VideoCapture(str(args.video.resolve()))
    frames = []
    try:
        for _ in range(args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            frames.append(frame)
    finally:
        capture.release()
    if not frames:
        raise RuntimeError("Video has no readable frames")
    model = str(args.model.resolve())
    variant = VariantCBackend(model, device="cpu")
    for frame in frames:
        variant.process_frame(frame)
    print(f"Association: PASS ({len(frames)} frames)")
    with tempfile.TemporaryDirectory(prefix="ppe-smoke-") as temporary:
        config = load_config(str(Path(__file__).resolve().parents[1] / "config.yaml"))
        config.model.path = model
        config.model.device = "cpu"
        config.storage.database = str(Path(temporary) / "events.db")
        config.storage.evidence_dir = str(Path(temporary) / "evidence")
        config.storage.save_evidence = False
        pipeline = PPEPipeline(config)
        try:
            for index, frame in enumerate(frames):
                pipeline.process_frame(frame, observed_at=index / 30)
            print(f"Research Event Engine: PASS ({len(frames)} frames)")
        finally:
            pipeline.repository.close()


if __name__ == "__main__":
    main()
