from scripts.check_docs import check_documents, heading_ids


def test_local_links_and_anchors(tmp_path):
    (tmp_path / "start.md").write_text(
        "[guide](<my guide.md#setup>)\n[repeat](my%20guide.md#setup-1)\n"
        "[web](https://example.com/missing)\n",
        encoding="utf-8",
    )
    (tmp_path / "my guide.md").write_text("# Setup\n## Setup\n", encoding="utf-8")
    assert check_documents(tmp_path, ["start.md"]) == []


def test_missing_target_and_anchor_are_errors(tmp_path):
    (tmp_path / "start.md").write_text(
        "# Start\n[missing](missing.md)\n[anchor](#unknown)\n", encoding="utf-8"
    )
    errors = check_documents(tmp_path, ["start.md"])
    assert len(errors) == 2
    assert any("missing target" in error for error in errors)
    assert any("missing heading" in error for error in errors)


def test_examples_in_code_are_ignored(tmp_path):
    (tmp_path / "start.md").write_text(
        "\x60\x60\x60md\n[fake](missing.md)\n\x60\x60\x60\n"
        "\x60[fake](missing.md)\x60\n",
        encoding="utf-8",
    )
    assert check_documents(tmp_path, ["start.md"]) == []


def test_nonportable_paths_are_errors(tmp_path):
    (tmp_path / "start.md").write_text(
        "[outside](../outside.md)\n[drive](C:/private/file.md)\n",
        encoding="utf-8",
    )
    assert len(check_documents(tmp_path, ["start.md"])) == 2


def test_unicode_and_duplicate_headings():
    assert heading_ids("# Bắt đầu\n# Bắt đầu\n") == {"bắt-đầu", "bắt-đầu-1"}


def test_inline_code_heading_keeps_its_text():
    assert heading_ids("# Run \x60ppe.py\x60\n") == {"run-ppepy"}
