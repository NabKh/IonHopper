# bhmc/core/bhmc.py
"""Basin Hopping Monte Carlo Core Implementation.

This module provides the core functionality for Basin Hopping Monte Carlo simulations. It implements a generic framework for structure optimization
and energy surface exploration.

Classes:
    Structure: Data structure for atomic configurations
    BasinHopping: Base class for BHMC implementation
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import logging
from pathlib import Path
import json

@dataclass
class Structure:
    """Atomic structure container.
    
    Attributes:
        positions: Atomic positions (N x 3 array)
        cell: Unit cell vectors (3 x 3 array)
        atomic_numbers: Atomic numbers (length N array)
        energy: Total energy of structure
    """
    positions: np.ndarray
    cell: np.ndarray
    atomic_numbers: np.ndarray
    energy: float = None
    
    def to_dict(self) -> Dict:
        """Convert structure to dictionary format."""
        return {
            'positions': self.positions.tolist(),
            'cell': self.cell.tolist(),
            'atomic_numbers': self.atomic_numbers.tolist(),
            'energy': self.energy
        }

class BasinHopping:
    """Base class for Basin Hopping Monte Carlo implementation.
    
    The algorithm performs Monte Carlo sampling of the potential energy surface,
    accepting or rejecting moves based on the Metropolis criterion.
    
    Args:
        temperature: Simulation temperature in Kelvin
        max_steps: Maximum number of Monte Carlo steps
        output_dir: Directory for output files
    """
    
    def __init__(self,
                 temperature: float = 300.0,
                 max_steps: int = 200,
                 output_dir: str = 'bhmc_results'):
        self.temperature = temperature
        self.max_steps = max_steps
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.current_step = 0
        self.accepted_steps = 0
        self.current_structure = None
        self.best_structure = None
        self.history: List[Structure] = []
        
        # Setup logging
        logging.basicConfig(
            filename=self.output_dir / 'bhmc.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def run(self, initial_structure: Structure) -> Structure:
        """Run Basin Hopping Monte Carlo simulation.
        
        Args:
            initial_structure: Starting atomic configuration
            
        Returns:
            Structure with lowest energy found
        """
        self.current_structure = initial_structure
        self.best_structure = initial_structure
        
        logging.info(f"Starting BHMC run at T={self.temperature}K")
        
        while self.current_step < self.max_steps:
            # Generate new structure
            new_structure = self._get_trial_structure()
            
            # Local optimization
            optimized_structure = self._local_optimization(new_structure)
            
            # Accept/reject step
            if self._accept_step(self.current_structure.energy,
                               optimized_structure.energy):
                self.current_structure = optimized_structure
                self.accepted_steps += 1
                
                if (optimized_structure.energy < 
                    self.best_structure.energy):
                    self.best_structure = optimized_structure
                    
            self.history.append(optimized_structure)
            self._save_step()
            self.current_step += 1
            
        logging.info(f"BHMC completed. Acceptance rate: "
                    f"{self.accepted_steps/self.max_steps:.2f}")
        return self.best_structure
    
    def _get_trial_structure(self) -> Structure:
        """Generate trial structure - implement in subclass."""
        raise NotImplementedError
        
    def _local_optimization(self, structure: Structure) -> Structure:
        """Perform local optimization - implement in subclass."""
        raise NotImplementedError
        
    def _accept_step(self, old_energy: float, 
                     new_energy: float) -> bool:
        """Metropolis acceptance criterion."""
        if new_energy <= old_energy:
            return True
        else:
            dE = new_energy - old_energy
            P = np.exp(-dE/(self.temperature * 8.617333262145e-5))
            return np.random.random() < P
            
    def _save_step(self):
        """Save current step information."""
        step_data = {
            'step': self.current_step,
            'energy': self.current_structure.energy,
            'best_energy': self.best_structure.energy,
            'structure': self.current_structure.to_dict(),
            'temperature': self.temperature,
            'accepted': self.accepted_steps
        }
        
        with open(self.output_dir / f'step_{self.current_step}.json', 
                 'w') as f:
            json.dump(step_data, f, indent=2)