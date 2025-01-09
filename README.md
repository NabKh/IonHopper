<div align="center">
  <svg viewBox="0 0 200 200">
    <!-- Modern gradient background -->
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#4a90e2;stop-opacity:0.05" />
        <stop offset="100%" style="stop-color:#50e3c2;stop-opacity:0.05" />
      </linearGradient>
    </defs>
    <!-- Background -->
    <rect width="200" height="200" fill="white" />
    <rect width="200" height="200" fill="url(#bg)" />
    <!-- Energy landscape curve -->
    <path d="M30,140 Q70,100 100,140 Q130,180 170,140" fill="none" stroke="#34495e" stroke-width="3" stroke-linecap="round" />
    <!-- Static ions -->
    <circle cx="70" cy="100" r="7" fill="#e74c3c" />
    <circle cx="100" cy="140" r="7" fill="#e74c3c" />
    <circle cx="130" cy="100" r="7" fill="#e74c3c" />
    <!-- Text -->
    <text x="100" y="60" text-anchor="middle" font-family="Helvetica" font-weight="bold" font-size="28">
      <tspan fill="#2c3e50">Ion</tspan>
      <tspan fill="#e74c3c">Hopper</tspan>
    </text>
  </svg>
  <h1>IonHopper</h1>
  <p>A Python framework implementing Basin Hopping Monte Carlo algorithm coupled with VASP for studying ion insertion in materials.</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
</div>

---

## Scientific Background

The investigation of ion insertion mechanisms in materials is fundamental to the development of next-generation energy storage systems. Understanding the structural evolution, phase stability, and thermodynamic properties during ion insertion/extraction processes requires accurate computational methods. Density functional theory (DFT) calculations have emerged as a powerful tool for studying these phenomena at the atomic scale.

However, traditional DFT approaches face significant challenges when exploring the vast configuration space of possible ion arrangements:

1. **Energy Landscape Complexity**
   - Multiple local minima in potential energy surface
   - Metastable configurations trap local optimization
   - Complex structural reorganization during ion insertion

2. **Configuration Space**
   - Exponential growth with system size
   - Manual structure generation introduces bias
   - Limited sampling of possible arrangements

3. **Phase Stability**
   - Multiple competing phases at each composition
   - Formation energy calculations require global minima
   - Voltage profiles depend on accurate phase identification

## Methodology

IonHopper implements the Basin Hopping Monte Carlo algorithm coupled with DFT calculations to address these challenges. The method:

1. **Energy Surface Transformation**
   - Maps continuous potential energy surface to discrete basins
   - Each basin corresponds to local minimum
   - Simplifies global optimization problem

2. **Monte Carlo Sampling**
   - Temperature-controlled acceptance criterion
   - Efficient exploration of configuration space
   - Escape from local minima

3. **DFT Integration**
   - Accurate energy evaluation using VASP
   - Structure optimization at each step
   - Electronic structure analysis

4. **Thermodynamic Analysis**
   - Convex hull construction
   - Phase stability determination
   - Voltage profile calculation

## Installation

```bash
git clone https://github.com/nabkh/ionhopper.git
cd ionhopper
pip install -e .
```

Requirements:
- Python ≥ 3.8
- ASE ≥ 3.22.1
- NumPy ≥ 1.21.0
- PyYAML ≥ 5.4.1
- VASP 5.4+ (not included)

## Quick Start

1. Configure calculation:
```bash
cp config.yaml.template config.yaml
# Edit settings
```

2. Prepare files:
```bash
python -m ionhopper.setup.prepare_calculation
```

3. Run BHMC:
```bash
python -m ionhopper.workflow.run_compositions --compositions 0.25 0.5 0.75 1.0
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Tutorial](docs/tutorial.md)
- [API Reference](docs/api)
- [Examples](examples/)

## Citation

If you use this code in your research, please cite:

```bibtex
@article{khossossi2022revealing,
  title={Revealing the superlative electrochemical properties of o-B2N2 monolayer in Lithium/Sodium-ion batteries},
  author={Khossossi, Nabil and Luo, Wei and Haman, Zakaryae and Singh, Deobrat and Essaoudi, Ismail and Ainane, Abdelmajid and Ahuja, Rajeev},
  journal={Nano Energy},
  volume={96},
  pages={107066},
  year={2022},
  publisher={Elsevier}
}

@article{khossossi2022flexible,
  title={Flexible 3D porous boron nitride interconnected network as a high-performance Li-and Na-ion battery electrodes},
  author={Khossossi, Nabil and Singh, Deobrat and Luo, Wei and Ahuja, Rajeev},
  journal={Electrochimica Acta},
  volume={421},
  pages={140491},
  year={2022},
  publisher={Elsevier}
}
```

## License

MIT License. See [LICENSE](LICENSE) file.
