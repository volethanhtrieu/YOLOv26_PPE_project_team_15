from backend.config import load_config


def test_full_profile_uses_chvg4_and_two_second_delay():
    config = load_config("config.yaml", profile="D_full_system")

    assert config.model.path == "weights/best.pt"
    assert config.classes.person == ["person"]
    assert config.classes.head == ["head"]
    assert config.classes.helmet == ["helmet"]
    assert config.classes.vest == ["vest"]
    assert config.event.enabled is True
    assert config.event.mode == "majority"
    assert config.event.voting_ratio == 0.70
    assert config.event.voting_window_seconds == 2.5
    assert config.event.violation_seconds == 2.0
    assert config.event.required_ppe == ["helmet", "vest"]
