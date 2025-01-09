# Basic Example: Na insertion in Graphene

This example demonstrates:
- Structure setup for 2D material
- BHMC calculation setup
- Running composition scanning
- Analyzing results

## Usage
1. Copy POSCAR and config.yaml
2. Edit config.yaml with your POTCAR path
3. Run:
```bash
python -m bhmc.setup.prepare_calculation
python -m bhmc.workflow.run_compositions --compositions 0.25 0.5
