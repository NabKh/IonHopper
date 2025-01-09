# bhmc/implementations/vasp_bhmc.py
"""VASP implementation of Basin Hopping Monte Carlo.

This module provides VASP-specific functionality for BHMC simulations,
handling structure optimization using VASP and file I/O operations.
"""

import numpy as np
from pathlib import Path
import subprocess
import shutil
from typing import List, Dict, Optional
from ase.io import read, write
from ase.io.vasp import write_vasp
from ..core import BasinHopping, Structure
import logging

class VASPBasinHopping(BasinHopping):
    """VASP-specific implementation of Basin Hopping Monte Carlo.
    
    Handles:
    - Structure manipulation for ion insertion
    - VASP calculation management
    - Energy extraction from OUTCAR
    
    Args:
        mobile_sites: Possible positions for mobile ions
        fixed_sites: Positions of fixed ions
        host_structure: Host lattice positions
        vasp_cmd: VASP execution command
    """
    
    def __init__(self,
                 mobile_sites: np.ndarray,
                 fixed_sites: np.ndarray,
                 host_structure: np.ndarray,
                 vasp_cmd: str = "mpprun vasp-gamma",
                 **kwargs):
        super().__init__(**kwargs)
        self.mobile_sites = mobile_sites
        self.fixed_sites = fixed_sites
        self.host = host_structure
        self.vasp_cmd = vasp_cmd
        
        # Copy VASP input files
        for file in ['INCAR', 'KPOINTS', 'POTCAR']:
            if Path(file).exists():
                shutil.copy(file, self.output_dir / file)
                
    def _get_trial_structure(self) -> Structure:
        """Generate new structure by moving random mobile ion."""
        new_positions = self.current_structure.positions.copy()
        
        # Select random mobile atom and new position
        mobile_idx = np.random.randint(len(self.mobile_sites))
        new_site = self.mobile_sites[
            np.random.randint(len(self.mobile_sites))]
            
        # Update position
        new_positions[mobile_idx] = new_site
        
        return Structure(
            positions=new_positions,
            cell=self.current_structure.cell,
            atomic_numbers=self.current_structure.atomic_numbers
        )
        
    def _local_optimization(self, structure: Structure) -> Structure:
        """Run VASP optimization for given structure."""
        # Create calculation directory
        calc_dir = self.output_dir / f'step_{self.current_step}'
        calc_dir.mkdir()
        
        # Copy input files
        for file in ['INCAR', 'KPOINTS', 'POTCAR']:
            shutil.copy(self.output_dir / file, calc_dir / file)
            
        # Write POSCAR
        self._write_poscar(structure, calc_dir / 'POSCAR')
        
        # Run VASP
        try:
            subprocess.run(self.vasp_cmd.split(), 
                         cwd=calc_dir, 
                         check=True,
                         capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"VASP failed: {e.output.decode()}")
            raise
            
        # Read results
        optimized = read(calc_dir / 'CONTCAR')
        energy = self._read_vasp_energy(calc_dir / 'OUTCAR')
        
        return Structure(
            positions=optimized.get_positions(),
            cell=optimized.get_cell(),
            atomic_numbers=optimized.get_atomic_numbers(),
            energy=energy
        )
        
    def _write_poscar(self, structure: Structure, filepath: Path):
        """Write VASP POSCAR with fixed and mobile atoms."""
        atoms = structure.positions
        all_positions = np.vstack([
            self.fixed_sites,
            atoms,
            self.host
        ])
        
        write_vasp(filepath,
                  atoms=all_positions,
                  cell=structure.cell,
                  direct=True)
                  
    @staticmethod
    def _read_vasp_energy(outcar_path: Path) -> float:
        """Extract total energy from VASP OUTCAR."""
        energy = None
        with open(outcar_path) as f:
            for line in f:
                if "TOTEN" in line:
                    energy = float(line.split()[4])
        if energy is None:
            raise ValueError("Energy not found in OUTCAR")
        return energy