# Theory

## Basin Hopping Monte Carlo
The Basin Hopping algorithm transforms the potential energy surface (PES) into a series of interpenetrating local minima. Key components:

1. Random Structure Generation
- Mobile ions randomly moved to allowed positions
- Host structure remains fixed

2. Local Optimization
- Each structure optimized using VASP
- Maps configuration to nearest local minimum

3. Metropolis Criterion
- Acceptance probability: P(E) = exp(-ΔE/kBT)
- Temperature controls acceptance rate

## Convex Hull Analysis
Identifies thermodynamically stable compositions:
- Points below hull line are stable phases
- Energy vs composition plotted
- Formation energies calculated relative to endpoints