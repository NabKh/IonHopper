# Usage Guide

## Installation
```bash
git clone https://github.com/yourusername/bhmc-vasp
cd bhmc-vasp
pip install -e .
```

## Configuration
1. Copy template: `cp config/config.yaml.template config.yaml`
2. Set POTCAR path and VASP parameters
3. Place POSCAR in working directory

## Running Calculations
```bash
# Prepare files
python -m bhmc.setup.prepare_calculation

# Run BHMC for compositions
python -m bhmc.workflow.run_compositions --compositions 0.25 0.5 0.75 1.0

# Check results/stable_configurations.json for stable phases
```

## Output Files
- step_*.json: Individual MC steps
- VASP files in step_* directories
- Convex hull results in results/