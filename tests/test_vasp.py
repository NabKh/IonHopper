# tests/test_vasp.py
import pytest
from bhmc.implementations import VASPBasinHopping
from pathlib import Path

def test_vasp_energy_reading(tmp_path):
    outcar = tmp_path / "OUTCAR"
    outcar.write_text("TOTEN  =     -100.123456")
    
    energy = VASPBasinHopping._read_vasp_energy(outcar)
    assert abs(energy - (-100.123456)) < 1e-6