"""Single entry point; each backend keeps its own working directory/imports."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "smoke-inference": (".", ["-m", "scripts.smoke_inference"]),
    "review-api": ("bytetrack_ppe", ["app.py"]),
    "dashboard": ("bytetrack_ppe", ["-m", "streamlit", "run", "dashboard.py"]),
    "infer": ("bytetrack_ppe", ["run_pipeline_safe.py"]),
    "wandb": ("bytetrack_ppe", ["wandb_live_inference.py"]),
    "ablation": ("bytetrack_ppe", ["evaluate_ablation.py"]),
    "event-api": (".", ["app.py"]),
    "event-video": (".", ["run_video.py"]),
    "check-model": (".", ["check_model.py"]),
    "association": (".", ["-m", "scripts.run_variant_c"]),
    "convert": (".", ["scripts/data/convert_chvg_to_4class.py"]),
    "validate": (".", ["scripts/data/validate_chvg_4class.py"]),
    "train": (".", ["scripts/train/train_chvg4.py"]),
    "test": (".", ["-m", "pytest", "tests"]),
}


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print("Usage: python ppe.py <command> [arguments]\n")
        for name, (directory, command) in COMMANDS.items():
            print(f"  {name:14} {directory}: {' '.join(command)}")
        print("\nUse absolute paths for video/model files. See docs/QUICKSTART.md.")
        return 0
    name = args.pop(0)
    if name not in COMMANDS:
        print(f"Unknown command: {name}", file=sys.stderr)
        return 2
    directory, command = COMMANDS[name]
    return subprocess.call([sys.executable, *command, *args], cwd=ROOT / directory)


if __name__ == "__main__":
    raise SystemExit(main())
