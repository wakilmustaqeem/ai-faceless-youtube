from scripts.generate_captions import generate_captions
from governance.captions_quality_gate import check_captions


def test_generated_captions_pass(tmp_path):
    path = tmp_path / "captions.srt"
    generate_captions(
        "First sentence. Second sentence with more words.",
        10.0,
        str(path),
    )
    result = check_captions(str(path), expected_duration=10.0)
    assert result["passed"] is True
    assert result["cue_count"] == 2
