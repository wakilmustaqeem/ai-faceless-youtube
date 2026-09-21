from governance import voice_quality_gate


def test_voice_gate_blocks_missing_audio(tmp_path):
    result = voice_quality_gate.check_voice(str(tmp_path / "missing.mp3"))
    assert result["passed"] is False
    assert result["reason"] == "audio_missing_or_empty"


def test_voice_gate_blocks_excessive_silence(monkeypatch, tmp_path):
    audio = tmp_path / "voice.mp3"
    audio.write_bytes(b"audio")

    class Result:
        returncode = 0
        stdout = "10.0\n"
        stderr = "silence_duration: 7.0\nmax_volume: -6.0 dB\n"

    def fake_run(*args, **kwargs):
        if "ffprobe" in args[0]:
            return Result()
        return Result()

    monkeypatch.setattr(voice_quality_gate.subprocess, "run", fake_run)
    result = voice_quality_gate.check_voice(str(audio))
    assert result["passed"] is False
    assert result["reason"] == "excessive_silence"


def test_voice_gate_passes_healthy_audio(monkeypatch, tmp_path):
    audio = tmp_path / "voice.mp3"
    audio.write_bytes(b"audio")

    class Probe:
        returncode = 0
        stdout = "10.0\n"
        stderr = ""

    class Analysis:
        returncode = 0
        stdout = ""
        stderr = "silence_duration: 1.0\nmax_volume: -3.0 dB\n"

    def fake_run(*args, **kwargs):
        return Probe() if "ffprobe" in args[0] else Analysis()

    monkeypatch.setattr(voice_quality_gate.subprocess, "run", fake_run)
    result = voice_quality_gate.check_voice(str(audio))
    assert result["passed"] is True
