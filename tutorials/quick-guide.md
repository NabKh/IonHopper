# Quick Start Guide for BHMC-VASP

## Setup Using Your POSCAR

1. **Create Working Directory**
```bash
mkdir bhmc_calculation
cd bhmc_calculation
mkdir results
```

2. **Copy Required Files**
```bash
# Copy your POSCAR
cp /path/to/your/POSCAR .

# Copy configuration template
cp /path/to/bhmc-vasp/config.yaml.template config.yaml
```

3. **Edit config.yaml**
```yaml
# Essential settings
potcar_path: "/path/to/vasp/potcar"
structure_file: "POSCAR"
mobile_element: "Na"     # or "Li"
base_sites: 5            # Number of sites for mobile ions

# VASP parameters
incar:
  ENCUT: 500
  EDIFF: 1.0E-6
  EDIFFG: -1.0E-2
  NSW: 50
  IBRION: 2
  ISIF: 2
```

4. **Prepare Files**
```bash
python -m bhmc.setup.prepare_calculation
```
This generates:
- INCAR
- KPOINTS
- POTCAR
- base, host, lattice1 files

5. **Run BHMC**
```bash
# Test single composition
python -m bhmc.workflow.run_compositions --compositions 0.25 --steps 10

# Full calculation
python -m bhmc.workflow.run_compositions --compositions 0.25 0.5 0.75 1.0 --steps 200
```

6. **Check Results**
```
results/
├── all_configurations.json     # All tested structures
└── stable_configurations.json  # Structures on convex hull

composition_*/                  # Individual VASP calculations
└── step_*/ 
    ├── POSCAR
    ├── CONTCAR
    └── OUTCAR
```

## Common Issues

- POTCAR Error: Check potcar_path in config.yaml
- VASP Error: Check INCAR parameters
- Memory Error: Reduce system size or increase computational resources