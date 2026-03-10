## Resources Catalog

### Summary
This document catalogs all resources gathered for the research project: "Convergence Rates in Chain-of-Thought Reasoning as Discrete Dynamical Systems." The hypothesis is that CoT prompting can be modeled as a discrete dynamical system on the Wasserstein space $\mathcal{P}(\Sigma^*)$, with convergence rates to fixed points characterized by spectral properties of transition operators.

### Papers
Total papers downloaded: 17

| # | Title | Authors | Year | File | Key Results |
|---|-------|---------|------|------|-------------|
| 1 | Metastable Dynamics of CoT Reasoning | Kim, Wu, Lee, Suzuki | 2025 | papers/2502.01694_metastable_dynamics_CoT.pdf | Power-law hitting time Θ̃(KM/ε); distillation achieves O(K) |
| 2 | Stochastic Dynamical Theory of LLM | Carson | 2025 | papers/2501.16783_stochastic_dynamical_LLM.pdf | SDE model, Fokker-Planck, phase transitions at α=β |
| 3 | Statistical Physics of LM Reasoning | Carson, Reisizadeh | 2025 | papers/2506.04374_statistical_physics_LM_reasoning.pdf | Regime-switching SLDS, R²=0.74, rank-40 projection |
| 4 | SDE Framework for LLM Interactions | Shukla, Joshi | 2025 | papers/2510.10739_SDE_framework_LLM.pdf | Eigenvalue-based convergence classification, ρ=-Re(λ_max) |
| 5 | Deep Equilibrium Models | Bai, Kolter, Koltun | 2019 | papers/1909.01377_deep_equilibrium_models.pdf | Fixed-point z*=f_θ(z*), implicit differentiation, spectral radius |
| 6 | Fixed Point Iterations in DNNs | Ke et al. | 2024 | papers/2410.11279_fixed_point_iterations_DNN.pdf | Exponential convergence K^L, multiple fixed points, perturbation bounds |
| 7 | Flow Models via Wasserstein Proximal GD | Cheng et al. | 2024 | papers/2310.17582_wasserstein_flow_convergence.pdf | Exponential W₂ convergence, O(log(1/ε)) JKO steps for O(ε²) KL |
| 8 | Wasserstein Gradient Flow Convergence | Various | 2025 | papers/2511.10884_wasserstein_gradient_flow_convergence.pdf | Accelerated convergence rates for Wasserstein gradient flows |
| 9 | Chain-of-Thought Prompting | Wei et al. | 2022 | papers/2201.11903_chain_of_thought_prompting.pdf | Foundational CoT paper |
| 10 | Markov Chain of Thought | Various | 2024 | papers/2410.17635_markov_chain_of_thought.pdf | MCoT with convergence to atomic forms |
| 11 | MARCOS: Markov Chain of Continuous Thoughts | Various | 2025 | papers/2509.25020_marcos_markov_continuous_thoughts.pdf | Continuous thought Markov chain |
| 12 | Atom of Thoughts | Various | 2025 | papers/2502.12018_atom_of_thoughts_markov.pdf | Markov decomposition to atomic reasoning |
| 13 | Dynamical Systems for Neural Networks | Chemnitz et al. | 2025 | papers/2507.05164_dynamical_systems_neural_nets.pdf | Mean-field limits, interacting particle systems |
| 14 | Transformers Learn Transfer Operators | Various | 2026 | papers/2602.18679_transformers_transfer_operators.pdf | Transfer/Koopman operators in-context |
| 15 | Mechanistic Transformers for Dynamical Systems | Various | 2025 | papers/2512.21113_mechanistic_transformers_dynamical.pdf | Mechanistic analysis |
| 16 | LLMs Learn Dynamical Systems | Various | 2024 | papers/2402.00795_LLMs_learn_dynamical_systems.pdf | In-context neural scaling law |
| 17 | Convergence of Training Transformers | Various | 2024 | papers/2409.17335_convergence_training_transformers.pdf | Non-asymptotic training convergence |

See papers/README.md for detailed descriptions.

### Prior Results Catalog

| Result | Source | Statement Summary | Used For |
|--------|--------|-------------------|----------|
| Banach Fixed-Point Theorem | Classical | Contractive f has unique fixed point; ‖x^(t)-p‖ ≤ K^t·C | Exponential convergence baseline |
| Fokker-Planck Stationary Distribution | Gardiner 2009 | P_ss(x) ∝ σ⁻²exp(2∫μ/σ²) | Equilibrium distribution of severity SDE |
| Brenier Theorem | Villani 2009 | Unique OT map T=∇φ exists between measures | Foundation for W₂ analysis |
| Ito SDE Well-Posedness | Oksendal 2003 | Lipschitz+linear growth → unique strong solution | Validating SDE models of CoT |
| Davis-Kahan Perturbation | Davis, Kahan 1970 | Eigenspace stability under perturbation | PCA projection stability |
| JKO Exponential Convergence | Cheng et al. 2024 | W₂(p_n,q) decays exponentially under λ-convexity a.g.g. | Wasserstein convergence rates |
| DEQ Implicit Gradient | Bai et al. 2019 | dℓ/d(·) = -(dℓ/dz*)J⁻¹·df/d(·) | Gradient through fixed points |
| Metastable Hitting Time | Kim et al. 2025 | E[τ] = Θ̃(KM/ε) for CoT Markov chains | Power-law convergence rate |
| Perturbed Fixed-Point Bound | Ke et al. 2024 | ‖x^(t)-p‖ ≤ K^t·C + O(1/m) with noise | Convergence with perturbation |
| Scaling Laws Near Criticality | Carson 2025 | ξ(Δ) ~ |Δ|^{-ν}, τ(Δ) ~ |Δ|^{-zν} | Phase transition characterization |

### Computational Tools

| Tool | Purpose | Location | Notes |
|------|---------|----------|-------|
| SymPy 1.14.0 | Symbolic computation | pip (in .venv) | Spectral analysis, operator algebra, symbolic ODEs |
| NumPy 2.4.3 | Numerical computation | pip (in .venv) | Eigenvalue computation, matrix operations |
| SciPy 1.17.1 | Scientific computing | pip (in .venv) | Sparse eigenvalue solvers, ODE integration |
| Matplotlib | Visualization | pip (in .venv) | Convergence rate plots, phase diagrams |
| NetworkX | Graph theory | pip (in .venv) | Transition graph structure, spectral graph theory |

### Resource Gathering Notes

#### Search Strategy
1. **Paper-finder** (Semantic Scholar): 5 diligent searches across CoT dynamics, Wasserstein convergence, iterative reasoning, spectral analysis, optimal transport
2. **Web search**: Targeted searches for recent arXiv papers on CoT as dynamical systems, fixed-point convergence, Wasserstein gradient flows
3. **arXiv direct**: Rate-limited, used web search as fallback
4. **Citation following**: Papers referenced in key papers (e.g., Bovier et al. metastability theory)

#### Selection Criteria
- Papers directly modeling CoT/LLM reasoning as dynamical systems (highest priority)
- Fixed-point convergence theory applicable to neural network inference
- Convergence analysis in Wasserstein space
- Spectral analysis of Markov chain transition operators
- Foundational CoT papers for context

#### Challenges Encountered
- arXiv API rate-limited (HTTP 429); used web search + direct downloads instead
- Paper-finder service timed out on some queries; fallback results still useful
- One paper (2502.05656) returned 404; excluded from collection

### Recommendations for Proof Construction

1. **Proof strategy:** Define the CoT operator $\mathcal{T}: \mathcal{P}_2(\Sigma^*) \to \mathcal{P}_2(\Sigma^*)$ as the pushforward of the conditional next-step distribution. Establish two convergence regimes:
   - **Exponential regime:** When $\mathcal{T}$ is contractive in $W_2$ (analogous to DEQ/Banach, spectral radius < 1), prove $W_2(\mathcal{T}^n\mu_0, \mu^*) \leq \kappa^n \cdot W_2(\mu_0, \mu^*)$.
   - **Power-law regime:** When metastability holds (cf. Kim et al.), prove hitting time $\Theta(KM/\varepsilon)$ and relate to Wasserstein distance decay via $W_2(\mu_n, \mu^*) = O(n^{-\alpha})$ for explicit $\alpha$.

2. **Key prerequisites:** Banach fixed-point theorem (exponential regime), Bovier metastability theory (power-law regime), Brenier theorem + $\lambda$-convexity a.g.g. (Wasserstein convergence), Fokker-Planck stationary distributions (equilibrium analysis).

3. **Computational tools:** Use SymPy to verify spectral properties of simple transition operators symbolically. Use NumPy/SciPy to numerically simulate toy Markov chains modeling CoT and measure convergence rates. Use NetworkX to analyze transition graph structure.

4. **Potential difficulties:**
   - Token sequence space is discrete; $W_2$ requires careful adaptation (embed via hidden states or use discrete OT metrics like Earth Mover's Distance)
   - General CoT operators may not be globally contractive; may need to establish contractivity only within basins of attraction
   - Connecting spectral gap of the transition operator to convergence rate requires the operator to be self-adjoint or at least quasi-compact (cf. non-reversible Markov chain theory)
   - The continuous-time SDE approximation introduces discretization error that must be bounded
