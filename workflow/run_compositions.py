# bhmc/workflow/run_compositions.py
"""Main workflow for BHMC composition scanning.

Manages multiple BHMC runs for different compositions and analyzes results.
"""

import argparse
import numpy as np
from pathlib import Path
import yaml
import json
from ase.io import read
from ..implementations.vasp_bhmc import VASPBasinHopping, Structure
from typing import List, Dict
import logging

def load_config(config_file: str = 'config.yaml') -> Dict:
    """Load configuration from YAML."""
    with open(config_file) as f:
        return yaml.safe_load(f)

def prepare_initial_structure(composition: float,
                            poscar_file: str,
                            config: Dict) -> Structure:
    """Create initial structure for given composition."""
    atoms = read(poscar_file)
    cell = atoms.get_cell()
    positions = atoms.get_positions()
    numbers = atoms.get_atomic_numbers()
    
    mobile_element = config['mobile_element']
    mobile_z = {'Li': 3, 'Na': 11}[mobile_element]
    
    mobile_sites = positions[numbers == mobile_z]
    n_mobile = int(composition * len(mobile_sites))
    
    selected_sites = mobile_sites[
        np.random.choice(len(mobile_sites), n_mobile, replace=False)]
    
    return Structure(
        positions=selected_sites,
        cell=cell,
        atomic_numbers=np.array([mobile_z] * n_mobile)
    )

def run_bhmc(composition: float, config: Dict, args: argparse.Namespace) -> Dict:
    """Run BHMC for single composition."""
    output_dir = f'composition_{composition:.2f}'
    
    init_structure = prepare_initial_structure(
        composition, config['structure_file'], config)
    
    bhmc = VASPBasinHopping(
        temperature=args.temp,
        max_steps=args.steps,
        output_dir=output_dir,
        mobile_sites=init_structure.positions,
        fixed_sites=np.array([]),
        host_structure=read(config['structure_file']).get_positions()
    )
    
    best_structure = bhmc.run(init_structure)
    
    return {
        'composition': composition,
        'energy': best_structure.energy,
        'structure': best_structure.to_dict()
    }

def analyze_stability(results: List[Dict]) -> List[Dict]:
    """Identify stable compositions using convex hull analysis."""
    stable = []
    compositions = [r['composition'] for r in results]
    energies = [r['energy'] for r in results]
    
    for i, result in enumerate(results):
        is_stable = True
        for j in range(len(results)):
            for k in range(j + 1, len(results)):
                if i != j and i != k:
                    x = result['composition']
                    y = result['energy']
                    x1, y1 = compositions[j], energies[j]
                    x2, y2 = compositions[k], energies[k]
                    
                    if x1 < x < x2:
                        y_hull = y1 + (y2-y1)*(x-x1)/(x2-x1)
                        if y > y_hull + 1e-6:  # Numerical tolerance
                            is_stable = False
                            break
            if not is_stable:
                break
        
        if is_stable:
            stable.append(result)
    
    return stable

def main():
    """Main workflow."""
    parser = argparse.ArgumentParser(description="BHMC composition scanning")
    parser.add_argument('--config', default='config.yaml',
                      help='Configuration file')
    parser.add_argument('--compositions', nargs='+', type=float,
                      help='Compositions to test')
    parser.add_argument('--temp', type=float, default=300,
                      help='Temperature (K)')
    parser.add_argument('--steps', type=int, default=200,
                      help='Number of steps')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    config = load_config(args.config)
    
    results = []
    for comp in args.compositions:
        logging.info(f"Starting composition x = {comp}")
        result = run_bhmc(comp, config, args)
        results.append(result)
    
    stable_results = analyze_stability(results)
    
    Path('results').mkdir(exist_ok=True)
    with open('results/all_configurations.json', 'w') as f:
        json.dump(results, f, indent=2)
    with open('results/stable_configurations.json', 'w') as f:
        json.dump(stable_results, f, indent=2)
    
    logging.info("Analysis complete. Check results/ directory.")

if __name__ == '__main__':
    main()