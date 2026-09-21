from governance import visual_quality_gate


def test_visual_gate_blocks_missing_video(tmp_path):
    result = visual_quality_gate.check_video(str(tmp_path / "missing.mp4"))
    assert result["passed"] is False
    assert result["reason"] == "video_missing_or_empty"


def test_visual_gate_blocks_extended_black(monkeypatch, tmp_path):
    video=tmp_path/"video.mp4"; video.write_bytes(b"video")
    class Result:
        returncode=0
        stdout="codec_type=video\n"
        stderr="black_duration:1.2\n"
    def fake_run(args, **kwargs):
        return Result()
    monkeypatch.setattr(visual_quality_gate.subprocess,"run",fake_run)
    result=visual_quality_gate.check_video(str(video))
    assert result["passed"] is False
    assert result["reason"]=="extended_black_frame"


def test_visual_gate_passes_clean_video(monkeypatch, tmp_path):
    video=tmp_path/"video.mp4"; video.write_bytes(b"video")
    class Probe:
        returncode=0; stdout="codec_type=video\n"; stderr=""
    class Analysis:
        returncode=0; stdout=""; stderr="black_duration:0.2\nfreeze_duration:0.8\n"
    def fake_run(args, **kwargs):
        return Probe() if "ffprobe" in args[0] else Analysis()
    monkeypatch.setattr(visual_quality_gate.subprocess,"run",fake_run)
    result=visual_quality_gate.check_video(str(video))
    assert result["passed"] is True
