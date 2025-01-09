# Installation Guide

## Prerequisites
1. Python 3.8 or higher
2. VASP 5.4+ with necessary licenses
3. Access to computational resources (HPC recommended)

## Environment Setup

### 1. Python Environment
```bash
# Create conda environment
conda create -n bhmc python=3.8
conda activate bhmc

# Alternative with venv
python -m venv bhmc-env
source bhmc-env/bin/activate  # Linux/Mac
.\bhmc-env\Scripts\activate   # Windows
```

### 2. BHMC-VASP Installation
```bash
# Clone repository
git clone https://github.com/Nabkh/bhmc-vasp.git
cd bhmc-vasp

# Install package
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### 3. VASP Setup
1. Ensure VASP is installed and accessible
2. Set VASP environment variables:
```bash
export VASP_PP_PATH=/path/to/potcar/files
export VASP_CMD="mpirun -np 4 vasp_std"
```

## Configuration

### 1. Basic Setup
```bash
# Copy template configuration
cp config.yaml.template config.yaml

# Edit config.yaml with your settings:
# - POTCAR path
# - Computational resources
# - VASP parameters
```

### 2. HPC Integration
For cluster environments:
1. Copy SLURM template:
```bash
cp config/slurm/submit.sh.template submit.sh
```

2. Modify job parameters:
```bash
# Edit submit.sh
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --time=48:00:00
```

## Testing Installation
```bash
# Run tests
pytest tests/

# Try example calculation
cd examples/basic
python -m bhmc.setup.prepare_calculation
python -m bhmc.workflow.run_compositions --compositions 0.25
```

## Common Issues

1. POTCAR Access
- Ensure valid VASP license
- Check POTCAR path in config.yaml
- Verify file permissions

2. VASP Execution
- Test VASP command directly
- Check MPI configuration
- Verify module loading on HPC

3. Python Dependencies
- Update pip: `pip install --upgrade pip`
- Check for conflicts: `pip check`
- Install missing dependencies: `pip install -r requirements.txt`