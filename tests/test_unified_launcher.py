from unittest.mock import patch

import ppe
from bytetrack_ppe.smoke_health import valid_health


def test_launcher_targets_exist():
    for directory, command in ppe.COMMANDS.values():
        if command[0] != "-m":
            assert (ppe.ROOT / directory / command[0]).is_file()


def test_launcher_uses_active_python_and_preserves_arguments():
    with patch("ppe.subprocess.call", return_value=7) as call:
        assert ppe.main(["infer", "--video", "C:/has space/video.mp4"]) == 7
    assert call.call_args.args[0] == [
        ppe.sys.executable, "run_pipeline_safe.py", "--video", "C:/has space/video.mp4"
    ]
    assert call.call_args.kwargs["cwd"] == ppe.ROOT / "bytetrack_ppe"


def test_unknown_command_fails():
    assert ppe.main(["nonexistent"]) == 2


class HealthResponse:
    def __init__(self, present, status, code):
        self.status_code = code
        self.payload = {
            "status": status,
            "sources": {
                key: {"exists": exists}
                for key, exists in zip(
                    ["events_json", "event_summary_json", "temporal_states_csv", "track_rows_csv"],
                    present,
                )
            },
        }

    def get_json(self, silent=False):
        return self.payload


def test_empty_health_is_explicit_opt_in():
    response = HealthResponse([False] * 4, "degraded", 503)
    assert not valid_health(response)
    assert valid_health(response, allow_empty=True)
    assert not valid_health(HealthResponse([True, False, False, False], "degraded", 503), allow_empty=True)
    assert valid_health(HealthResponse([True] * 4, "ok", 200))
    assert not valid_health(HealthResponse([True] * 4, "ok", 503))
