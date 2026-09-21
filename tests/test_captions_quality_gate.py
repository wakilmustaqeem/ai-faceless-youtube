from governance.captions_quality_gate import check_captions


def test_missing_captions_block():
    result = check_captions("missing.srt")
    assert result["passed"] is False
    assert result["reason"] == "captions_missing_or_empty"


def test_overlapping_captions_block(tmp_path):
    path = tmp_path / "captions.srt"
    path.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nFirst\n\n"
        "2\n00:00:01,500 --> 00:00:03,000\nSecond\n",
        encoding="utf-8",
    )
    result = check_captions(str(path))
    assert result["passed"] is False
    assert result["reason"] == "caption_overlap"


def test_clean_captions_pass(tmp_path):
    path = tmp_path / "captions.srt"
    path.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nFirst caption.\n\n"
        "2\n00:00:02,500 --> 00:00:04,000\nSecond caption.\n",
        encoding="utf-8",
    )
    result = check_captions(str(path), expected_duration=4.0)
    assert result["passed"] is True
