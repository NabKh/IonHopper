# tests/test_workflow.py
import pytest
from bhmc.workflow.run_compositions import analyze_stability

def test_convex_hull():
    results = [
        {"composition": 0.0, "energy": 0.0},
        {"composition": 0.5, "energy": -1.0},
        {"composition": 1.0, "energy": -0.5}
    ]
    
    stable = analyze_stability(results)
    assert len(stable) == 3