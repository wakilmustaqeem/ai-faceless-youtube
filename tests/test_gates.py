from governance import human_review, originality_gate, publish_gate


def test_human_review_blocks_unreviewed():
    assert human_review.decision(False, False)["status"] == "BLOCKED"


def test_originality_blocks_until_engine_configured():
    assert originality_gate.check("sample")["passed"] is False


def test_publish_is_disabled_by_default():
    result = publish_gate.can_publish(True, True, True)
    assert result["allowed"] is False
