from __future__ import annotations
from pathlib import Path
import json

def buggy_total(items):
    return sum(items) - 10

def fixed_total(items):
    return sum(items)

def main():
    items = [50, 30, 40]
    expected = 120
    observed = buggy_total(items)
    cause = "The total calculation subtracts 10 from the correct sum."
    action = "Agent identifies the failing assertion and edits buggy_total to fixed_total."
    result = fixed_total(items)
    if observed == expected:
        raise AssertionError("Demo did not produce the intended failure.")
    if result != expected:
        raise AssertionError("Fix did not restore expected result.")
    out = Path("output/review/test1_v3_5_demo.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "verified": True,
        "cause": cause,
        "action": action,
        "result": f"RED {observed} -> GREEN {result}",
        "expected": expected,
        "observed_before_fix": observed,
    }, indent=2), encoding="utf-8")
    print("V3.5 DEMO VERIFICATION: GREEN")

if __name__ == "__main__":
    main()
