# Convergence Rates in Chain-of-Thought Reasoning as Discrete Dynamical Systems

Mathematical analysis of chain-of-thought (CoT) prompting modeled as a discrete Markov dynamical system on probability distributions, with rigorous convergence rate bounds characterized by spectral properties of the transition operator.

## Key Results

- **Theorem 1:** Exponential convergence W₁(Tⁿμ₀, μ*) ≤ δ(P)ⁿ · W₁(μ₀, μ*) under Dobrushin contraction
- **Theorem 2:** W₂ convergence rate is (1-γ)^{1/2} where γ is the spectral gap (verified: r = 0.979)
- **Theorem 3:** Exact spectral gap γ = Kε/(K-1) for (K,ε)-metastable chains (matches numerics exactly)
- **Theorem 4:** Phase transition at critical coupling ε_c = (K-1)γ_intra/K between slow/fast regimes
- **Proposition 1:** Bifurcation analysis showing convergence failure below critical inter-basin coupling

## Computational Verification

Six experiments validate the theoretical predictions:
1. Contractive convergence rates match √(1-γ) prediction to 3 decimal places
2. Metastable spectral gaps match Kε/(K-1) formula exactly
3. Phase transition identified at ε ≈ 0.62 for K=3 model
4. Spectral gap–convergence rate correlation: r = 0.979 across 30 random matrices
5. Bifurcation threshold confirmed at coupling c ≈ 0.05
6. Complexity scaling: spectral gap saturates as K → ∞

## Repository Structure

```
├── REPORT.md              # Full mathematical report with proofs
├── planning.md            # Research plan and motivation
├── definitions.md         # Formal definitions and notation
├── src/
│   ├── convergence_verification.py   # All computational experiments
│   └── make_figures.py               # Figure generation
├── results/
│   └── all_results.json              # Raw experimental data
├── figures/
│   ├── fig1_contractive_convergence.png
│   ├── fig2_spectral_gap_correlation.png
│   ├── fig3_metastable_regime.png
│   ├── fig4_phase_transition.png
│   ├── fig5_bifurcation.png
│   └── fig6_complexity_scaling.png
├── papers/                # Reference papers (17 PDFs)
└── literature_review.md   # Synthesized literature review
```

## Reproducing Results

```bash
# Setup
uv venv && source .venv/bin/activate
uv add numpy scipy matplotlib networkx sympy

# Run experiments
python src/convergence_verification.py

# Generate figures
python src/make_figures.py
```

## Full Details

See [REPORT.md](REPORT.md) for complete proofs, computational verification, and discussion.
