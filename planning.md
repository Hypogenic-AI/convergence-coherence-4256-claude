# Research Plan: Convergence Rates in Chain-of-Thought Reasoning as Discrete Dynamical Systems

## Motivation & Novelty Assessment

### Why This Research Matters
Chain-of-thought prompting is the dominant technique for improving LLM reasoning, yet lacks rigorous mathematical foundations for understanding *why* and *when* iterative reasoning converges to correct answers. A formal convergence theory would provide: (1) fundamental limits on how many reasoning steps are needed, (2) criteria for when reasoning will succeed vs. fail, and (3) principled design of prompting strategies based on dynamical systems properties.

### Gap in Existing Work
From the literature review, three critical gaps exist:
1. **No formal W₂ convergence analysis of CoT.** Cheng et al. (2024) prove exponential convergence in Wasserstein space for flow-based models, but this has not been applied to autoregressive CoT.
2. **Spectral theory of CoT operators is undeveloped.** Kim et al. (2025) use pseudo-spectral gaps for within-cluster mixing, and Shukla & Joshi (2025) classify convergence by eigenvalues of linearized drift, but no comprehensive spectral characterization of the CoT transition operator exists.
3. **Power-law vs. exponential convergence regimes are uncharacterized.** Kim et al. show power-law Θ̃(KM/ε) hitting times; Ke et al. and DEQ show exponential K^t convergence. The conditions separating these regimes are unknown.

### Our Novel Contribution
We provide a unified mathematical framework that:
1. Formalizes CoT as a Markov operator T on probability measures over an embedded state space with Wasserstein-2 metric
2. Proves existence/uniqueness of fixed points under explicit contraction conditions
3. Derives **two distinct convergence regimes** with explicit rate bounds:
   - Exponential: W₂(T^n μ₀, μ*) ≤ κⁿ · W₂(μ₀, μ*) when T is κ-contractive
   - Power-law: W₂(T^n μ₀, μ*) = O(n^{-α}) in metastable regime with α depending on spectral gap ratio
4. Characterizes the phase transition between regimes via a critical contraction parameter
5. Validates predictions computationally on synthetic Markov chain models

### Experiment Justification
- **Experiment 1 (Contractive regime simulation):** Verify exponential convergence rate prediction W₂ ~ κⁿ by constructing a toy contractive Markov operator and measuring convergence.
- **Experiment 2 (Metastable regime simulation):** Verify power-law convergence by constructing a metastable Markov chain with cluster structure and measuring W₂ decay.
- **Experiment 3 (Phase transition):** Vary contraction parameter across critical threshold to observe transition between exponential and power-law regimes.
- **Experiment 4 (Spectral gap validation):** Compute spectral gaps of transition matrices and verify predicted relationship to convergence rates.

## Research Question
Can the convergence behavior of chain-of-thought reasoning be rigorously characterized as a discrete dynamical system, with explicit convergence rate bounds determined by spectral properties of the transition operator?

## Hypothesis Decomposition

### Sub-hypothesis 1: Well-posedness
The CoT transition operator T: P₂(X) → P₂(X) is well-defined on the Wasserstein-2 space of probability measures over an appropriate state space X, and preserves finite second moments.

### Sub-hypothesis 2: Fixed-point existence
Under appropriate conditions on the transition kernel, T admits at least one fixed point μ* ∈ P₂(X). Under stronger contraction conditions, the fixed point is unique.

### Sub-hypothesis 3: Exponential convergence
When T is κ-contractive in W₂ (κ < 1), iterates converge exponentially: W₂(Tⁿμ₀, μ*) ≤ κⁿ · W₂(μ₀, μ*).

### Sub-hypothesis 4: Power-law convergence in metastable regime
When the state space has metastable cluster structure with K clusters and within-cluster mixing time proportional to M/ε, the W₂ convergence follows a power-law: W₂(Tⁿμ₀, μ*) = O(n^{-1/2} · (KM/ε)^{1/2}).

### Sub-hypothesis 5: Spectral characterization
The convergence rate is determined by the spectral gap γ of T: exponential rate = 1 - γ in the contractive regime, and the ratio of inter-cluster to intra-cluster spectral gaps determines the power-law exponent.

## Proposed Methodology

### Approach
Model CoT reasoning on a finite state space S (representing embedded reasoning states) with a transition kernel defining operator T. Work in discrete probability space with earth mover's distance (discrete W₁ or W₂). This avoids the difficulty of continuous Wasserstein space on token sequences while preserving the essential dynamical structure.

### Proof Strategy
1. **Definitions:** State space, transition operator, Wasserstein metric on finite spaces
2. **Lemma 1 (Well-posedness):** T maps P(S) to P(S), is continuous in W₂
3. **Lemma 2 (Contraction):** Under Dobrushin coefficient < 1, T is W₁-contractive
4. **Theorem 1 (Exponential convergence):** Banach fixed-point theorem gives unique fixed point with exponential convergence
5. **Theorem 2 (Spectral decomposition):** Relate convergence rate to second-largest eigenvalue of transition matrix
6. **Theorem 3 (Metastable regime):** For block-structured transition matrices with weak inter-block coupling, derive power-law W₂ convergence bounds
7. **Theorem 4 (Phase transition):** Characterize critical coupling strength separating exponential from power-law regimes

### Computational Verification
- Construct explicit transition matrices for toy CoT models
- Compute eigenvalues, Dobrushin coefficients, and spectral gaps
- Simulate Markov chains and measure W₂ convergence rates
- Fit convergence curves to verify exponential vs. power-law predictions

### Evaluation Metrics
- Spectral gap of transition operator (computed exactly for small systems)
- Dobrushin contraction coefficient
- W₂ distance decay rate (measured from simulation)
- Goodness-of-fit (R²) for exponential and power-law models

## Timeline
- Phase 1 (Planning): 15 min ✓
- Phase 2 (Setup & Definitions): 15 min
- Phase 3 (Proof Construction): 90 min
- Phase 4 (Computational Verification): 45 min
- Phase 5 (Refinement): 20 min
- Phase 6 (Documentation): 25 min

## Potential Challenges
1. Dobrushin contraction may be too restrictive — may need weaker Lyapunov conditions
2. Power-law convergence bounds may be loose — tightness analysis needed
3. Phase transition may not be sharp — could be a crossover region
4. Discrete W₂ computation is O(n³) — limit state space size

## Success Criteria
- At least 2 rigorous theorems with complete proofs
- Computational verification showing predicted rates match simulation
- Clear characterization of at least 2 convergence regimes
