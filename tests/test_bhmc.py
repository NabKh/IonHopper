# tests/test_bhmc.py
import pytest
import numpy as np
from bhmc.core import BasinHopping, Structure

def test_structure_creation():
    positions = np.array([[0, 0, 0], [1, 1, 1]])
    cell = np.eye(3)
    numbers = np.array([1, 1])
    
    structure = Structure(positions, cell, numbers)
    assert np.array_equal(structure.positions, positions)

def test_metropolis_criterion():
    class TestBH(BasinHopping):
        def _get_trial_structure(self): pass
        def _local_optimization(self, s): pass
    
    bh = TestBH(temperature=100)
    assert bh._accept_step(-1.0, -1.5) == True
    assert bh._accept_step(-1.0, -0.5) == False