"""Readiness validation for both published and explicitly empty-checkout tests."""


def valid_health(response, *, allow_empty=False):
    payload = response.get_json(silent=True) or {}
    sources = payload.get("sources", {})
    expected_keys = {
        "events_json", "event_summary_json", "temporal_states_csv", "track_rows_csv"
    }
    if set(sources) != expected_keys:
        return False
    ready = all(item.get("exists") is True for item in sources.values())
    if ready:
        return response.status_code == 200 and payload.get("status") == "ok"
    return (
        allow_empty
        and all(item.get("exists") is False for item in sources.values())
        and response.status_code == 503
        and payload.get("status") == "degraded"
    )
