## Literature Review: Convergence Rates in Chain-of-Thought Reasoning as Discrete Dynamical Systems

### Research Area Overview

This review surveys the mathematical foundations for modeling chain-of-thought (CoT) prompting as a discrete dynamical system on probability distributions over token sequences. The research hypothesis posits that iterative reasoning steps exhibit measurable convergence rates to fixed points (correct solutions), following power-law or exponential decay patterns characterized by spectral properties of transition operators. The relevant literature spans four areas: (1) dynamical systems models of LLM reasoning, (2) fixed-point theory in deep networks, (3) convergence in Wasserstein space, and (4) spectral analysis of Markov chains/transition operators.

---

### Key Definitions

**Definition 1 (Chain-of-Thought as Markov Chain).** CoT generation is modeled as a discrete-time Markov chain $X^\varepsilon = (X^\varepsilon_t)_{t \geq 0}$ on a finite state space $\mathcal{S}$ of logical assertions, with transition kernel $p^\varepsilon$ parametrized by a difficulty parameter $\varepsilon > 0$. States represent sentences or mathematical expressions; transitions represent reasoning steps. (Kim, Wu, Lee, Suzuki 2025)

**Definition 2 (Metastable System).** A subset $\mathcal{M} \subset \mathcal{S}$ is metastable if $\lim_{\varepsilon \to 0} \sup_{x \in \mathcal{M}, y \notin \mathcal{M}} P_x(\bar{\tau}^\varepsilon_{\mathcal{M}\setminus\{x\}} < \bar{\tau}^\varepsilon_x) / P_y(\bar{\tau}^\varepsilon_{\mathcal{M}} < \bar{\tau}^\varepsilon_y) = 0$. That is, returning to $\mathcal{M}$ is much easier than transitioning between states in $\mathcal{M}$. (Bovier et al. 2002, applied in Kim et al. 2025)

**Definition 3 (Severity SDE).** An instantaneous severity variable $x(t) \in [0,1]$ evolves under $dx(t) = \mu(x(t))\,dt + \sigma(x(t))\,dW(t)$, where $\mu(x) = \alpha x(1-x) - \beta x^2 + \gamma$ (logistic self-reinforcement minus alignment damping), and $\sigma(x) = \sigma_0 + \sigma_1 x$. (Carson 2025)

**Definition 4 (Sentence-Stride Process).** The discrete sequence $\{h_t\}_{t \in \mathbb{N}}$ obtained by extracting the final-layer transformer state at each sentence boundary, modeling mesoscopic semantic-level reasoning dynamics. (Carson & Reisizadeh 2025)

**Definition 5 (Regime-Switching SDE).** Let $Z(t) \in \{1,\ldots,K\}$ be a latent continuous-time Markov chain with rate matrix $\mathbf{T}$. The regime-switching Ito SDE is $dh(t) = \mu_{Z(t)}(h(t))\,dt + B_{Z(t)}(h(t))\,dW(t)$, with per-regime drift and diffusion. (Carson & Reisizadeh 2025)

**Definition 6 (Deep Equilibrium Model).** The fixed point $z^*_{1:T} = f_\theta(z^*_{1:T}; x_{1:T})$ of a weight-tied deep sequence model, corresponding to the limit of infinite-depth iteration. (Bai, Kolter, Koltun 2019)

**Definition 7 (Wasserstein-2 Distance).** $W_2^2(\mu, \nu) := \inf_{\pi \in \Pi(\mu,\nu)} \int \|x - y\|^2\,d\pi(x,y)$, where $\Pi(\mu,\nu)$ is the set of all couplings. (Villani 2009)

**Definition 8 ($\lambda$-Convexity Along Generalized Geodesics).** A functional $\phi$ on $\mathcal{P}_2(\mathbb{R}^d)$ is $\lambda$-convex a.g.g. if $\phi(\mu^{1 \to 2}_t) \leq (1-t)\phi(\mu_1) + t\phi(\mu_2) - \frac{\lambda}{2}t(1-t)W^2_\nu(\mu_1,\mu_2)$. (Cheng, Lu, Tan, Xie 2024)

**Definition 9 (Pseudo-Spectral Gap).** For a stochastic complement $S^\varepsilon_{kk}$, the pseudo-spectral gap $\gamma^\dagger(S^\varepsilon_{kk}) \geq \gamma > 0$ controls within-cluster mixing time. (Kim et al. 2025)

**Definition 10 (Looped Neural Network).** Given weight matrix $W$, bias $b$, activation $g$, define $f(x; W, b) := g(Wx + b)$ and iterate $x^{(t)} := f(x^{(t-1)}; W, b)$ for $t \in [L]$. (Ke et al. 2024)

---

### Key Papers

#### Paper 1: Metastable Dynamics of Chain-of-Thought Reasoning (Kim, Wu, Lee, Suzuki, 2025)
- **arXiv:** 2502.01694
- **Main Results:**
  - **Theorem 3.2 (Expected Hitting Time):** Under metastability assumptions, $\mathbb{E}[\tau^\varepsilon_{X_{\text{out}}}] = \tilde{\Theta}(KM/\varepsilon)$ where $K$ = number of reasoning clusters, $M$ = cluster size, $\varepsilon$ = sparse edge probability. This is a **power-law** rate in $1/\varepsilon$.
  - **Theorem 4.3 (Distilled CoT):** Distilled meta-chain achieves $\mathbb{E}[\tau^+] = O(K)$, eliminating dependence on $\varepsilon$ and $M$.
  - **Corollary 5.6 (Hardness):** Without global search, any parametric model requires $\exp(\Omega(K))$ queries — exponential lower bound.
- **Proof Techniques:** Stochastic complement decomposition, metastability theory (Bovier et al.), SQ dimension analysis, PPO-Clip convergence analysis.
- **Relevance:** Directly models CoT as a Markov chain with metastable clusters, proving power-law convergence rates. Most directly relevant paper to our hypothesis.

#### Paper 2: A Stochastic Dynamical Theory of LLM Self-Adversariality (Carson, 2025)
- **arXiv:** 2501.16783
- **Main Results:**
  - Fokker-Planck equation for probability density over severity: $\partial_t P = -\partial_x[\mu(x)P] + \frac{1}{2}\partial_x^2[\sigma^2(x)P]$
  - Stationary distribution: $P_{\text{ss}}(x) \propto \frac{1}{\sigma^2(x)}\exp\left(2\int_0^x \frac{\mu(z)}{\sigma^2(z)}\,dz\right)$
  - Phase transition at $\alpha = \beta$: subcritical (convergent, self-correcting) vs. supercritical (runaway)
  - Scaling laws near criticality: $\xi(\Delta) \sim |\Delta|^{-\nu}$, $\tau(\Delta) \sim |\Delta|^{-z\nu}$
- **Proof Techniques:** SDE/Fokker-Planck analysis, potential landscape analysis, nonequilibrium phase transition theory.
- **Relevance:** Provides the continuous-time SDE framework for modeling CoT as a dynamical process, with explicit convergence/divergence criteria.

#### Paper 3: A Statistical Physics of Language Model Reasoning (Carson & Reisizadeh, 2025)
- **arXiv:** 2506.04374
- **Main Results:**
  - Rank-40 PCA projection captures ~50% variance of sentence-level hidden state trajectories
  - 4 latent reasoning regimes identified via GMM on projected residuals
  - SLDS model achieves $R^2 \approx 0.74$ for one-step-ahead prediction (vs. 0.51 for single linear model)
  - Projection leakage bound: $\mathcal{L}_k(\varepsilon) \leq L_\mu \varepsilon / \mu_{\min}$
- **Proof Techniques:** Ito SDE well-posedness via Picard iteration, Davis-Kahan perturbation theory for PCA stability, EM algorithm for SLDS fitting.
- **Relevance:** Empirically validates the SDE framework across 8 models and 7 benchmarks, providing the regime-switching model that captures distinct reasoning phases.

#### Paper 4: Deep Equilibrium Models (Bai, Kolter, Koltun, 2019)
- **arXiv:** 1909.01377
- **Main Results:**
  - **Theorem 1 (Gradient):** $\frac{d\ell}{d(\cdot)} = -\frac{d\ell}{dz^*} J^{-1}_{g_\theta}\big|_{z^*} \frac{df_\theta}{d(\cdot)}$ via implicit differentiation
  - **Theorem 2 (Universality):** Stacking DEQs does not add representational power
  - Convergence depends on contractivity: spectral radius of Jacobian $J_{f_\theta} < 1$
- **Proof Techniques:** Implicit function theorem, Broyden's method with Sherman-Morrison updates.
- **Relevance:** Provides the fixed-point framework for modeling transformer inference as convergence to equilibrium, with spectral radius as the key convergence parameter.

#### Paper 5: Fixed Point Iterations in Deep Neural Networks (Ke et al., 2024)
- **arXiv:** 2410.11279
- **Main Results:**
  - **Theorem 4.1 (Multiple Fixed Points):** Looped neural networks can have at least $m$ fixed points with exponential convergence $\|x^{(L)} - p_i\|_\infty \leq K_i^L \cdot c_i \cdot \varepsilon_i$ where $K_i < 1$.
  - **Theorem 4.2 (Perturbed Iteration):** With noise $|h(x)| \leq 1/m$: $|x^{(t)} - p| \leq K^t|x^{(0)} - p| + 20/m$ — exponential decay to noise floor.
  - Up to $2^d$ robust fixed points with polynomial/exponential activations.
- **Proof Techniques:** Banach contraction mapping theorem, Jacobian-based contractivity verification.
- **Relevance:** Establishes exponential convergence rates for fixed-point iterations in neural networks, with explicit spectral (contractivity) conditions.

#### Paper 6: Convergence of Flow-Based Generative Models in Wasserstein Space (Cheng et al., 2024)
- **arXiv:** 2310.17582
- **Main Results:**
  - JKO proximal gradient descent in $W_2$ achieves **exponential convergence**: both $W_2(p_n, q)$ and $G(p_n) - G(q)$ decay exponentially
  - $N \leq O(\log(1/\varepsilon))$ JKO steps suffice for $O(\varepsilon^2)$ KL error
  - $\lambda$-convexity along generalized geodesics is the key structural condition
- **Proof Techniques:** Wasserstein proximal operator analysis, Brenier theorem, data processing inequality.
- **Relevance:** Provides rigorous convergence rates in Wasserstein space for iterative schemes — the mathematical framework for our hypothesis about convergence on probability distributions.

#### Paper 7: SDE Framework for Multi-Objective LLM Interactions (Shukla & Joshi, 2025)
- **arXiv:** 2510.10739
- **Main Results:**
  - Convergence rate $\rho = -\text{Re}(\lambda_{\max})$ where $\lambda_{\max}$ is the dominant eigenvalue of drift matrix $A$
  - Three dynamical regimes: exponential convergence ($\lambda_i$ real negative), oscillatory ($\lambda$ complex), boundary attraction ($\lambda \approx 0$)
  - Discrete stability: $|\lambda_{\text{discrete}}| = |1 + \lambda_{\text{continuous}} \Delta t| < 1$
- **Proof Techniques:** Euler-Maruyama discretization, eigenvalue classification of linearized drift.
- **Relevance:** Directly applies spectral analysis of transition operators to classify convergence behavior of iterative LLM processes.

#### Paper 8: Chain-of-Thought Prompting Elicits Reasoning (Wei et al., 2022)
- **arXiv:** 2201.11903
- **Relevance:** Foundational paper establishing CoT prompting. Provides empirical evidence that multi-step reasoning improves LLM performance on complex tasks — the phenomenon our mathematical framework aims to explain.

#### Paper 9: Markov Chain of Thought for Efficient Mathematical Reasoning (2024)
- **arXiv:** 2410.17635
- **Main Results:** Conceptualizes CoT as a Markov chain with "derive then reduce" logic. Deeper reasoning states converge to irreducible (atomic) forms with stable token counts.
- **Relevance:** Empirical validation of the Markov chain model for CoT, supporting the discrete dynamical systems perspective.

---

### Known Results (Prerequisite Theorems)

**Theorem (Banach Fixed-Point).** If $f: D \to D$ is contractive with constant $K < 1$, then $f$ has a unique fixed point $p$ and $\|x^{(t)} - p\| \leq K^t/(1-K)\|x^{(1)} - x^{(0)}\|$. *Rate: exponential.*

**Theorem (Fokker-Planck Stationary Distribution).** For SDE $dx = \mu(x)dt + \sigma(x)dW$, the stationary density is $P_{\text{ss}}(x) \propto \sigma^{-2}(x)\exp(2\int_0^x \mu(z)/\sigma^2(z)\,dz)$.

**Theorem (Brenier).** For $\mu \in \mathcal{P}_2^r$ and $\nu \in \mathcal{P}_2$, there exists a unique optimal transport map $T^\nu_\mu = \nabla\phi$ ($\phi$ convex).

**Theorem (Ito SDE Well-Posedness, Oksendal 2003).** Under Lipschitz continuity and linear growth of $\mu$ and $B$, the SDE has a unique strong solution.

**Theorem (Davis-Kahan).** The sine of the angle between empirical and population eigenspaces is bounded by $O(\|\Delta\|/\delta)$ where $\delta$ is the spectral gap, ensuring PCA stability.

**Theorem (JKO Convergence).** Under $\lambda$-convexity a.g.g. of the KL functional, the JKO scheme converges exponentially: $W_2(p_n, q) \leq C \cdot e^{-\lambda n}$ and $\text{KL}(p_n\|q) = O(\varepsilon^2)$ in $N = O(\log(1/\varepsilon))$ steps.

---

### Proof Techniques in the Literature

- **Metastability and stochastic complements** (Kim et al.): Decomposing the state space into clusters with fast within-cluster mixing and slow inter-cluster transitions. Uses pseudo-spectral gaps to bound intra-cluster convergence.
- **SDE/Fokker-Planck analysis** (Carson): Continuous-time diffusion limits of discrete token generation, potential landscape analysis for phase classification.
- **Contraction mapping arguments** (Ke et al., Bai et al.): Proving convergence via Jacobian spectral radius bounds; Banach theorem gives exponential rates.
- **Wasserstein proximal gradient descent** (Cheng et al.): Proving convergence of iterative transport maps using $\lambda$-convexity in $W_2$.
- **Eigenvalue/spectral decomposition** (Shukla & Joshi): Classifying convergence regimes by the eigenvalue spectrum of the drift matrix.
- **Regime-switching models** (Carson & Reisizadeh): EM algorithm for SLDS fitting, GMM for latent regime identification.

---

### Related Open Problems

1. **Formal convergence rates for CoT in Wasserstein space.** No existing paper proves that CoT iterates converge in $W_2$ to a fixed-point distribution. The JKO scheme results (Cheng et al.) apply to flow-based models but not directly to autoregressive CoT.
2. **Spectral characterization of the CoT transition operator.** The pseudo-spectral gap (Kim et al.) controls within-cluster mixing, but the full spectral decomposition of the CoT transition operator — especially its relationship to power-law vs. exponential convergence — remains open.
3. **Power-law vs. exponential convergence regimes.** Kim et al. show power-law $\tilde{\Theta}(KM/\varepsilon)$ hitting times (suggesting power-law convergence). Ke et al. and DEQ show exponential convergence under contractivity. The conditions determining which regime applies to CoT are not characterized.
4. **Non-Markovian extensions.** All current models assume (approximate) Markov dynamics. Real CoT involves long-range dependencies. Memory kernels or fractional dynamics may be needed.
5. **Bridging discrete and continuous models.** The SDE/Fokker-Planck framework (Carson) uses continuous-time limits, while the Markov chain model (Kim et al.) is discrete. A unified framework connecting both with explicit error bounds for the continuous approximation is lacking.

---

### Gaps and Opportunities

- **Gap 1:** No paper directly models CoT on the **Wasserstein space of probability distributions** over token sequences with formal convergence analysis. The hypothesis of this research project fills precisely this gap.
- **Gap 2:** The spectral theory of CoT transition operators is undeveloped. While spectral gaps appear in metastability theory (Kim et al.) and eigenvalue analysis appears in linearized SDEs (Shukla & Joshi), a comprehensive spectral characterization linking convergence rates to operator properties is missing.
- **Gap 3:** The relationship between power-law convergence (metastable regime) and exponential convergence (contractive regime) has not been mapped as a function of model/problem parameters.

---

### Recommendations for Proof Strategy

1. **Recommended approach:** Model the CoT reasoning process as a discrete-time Markov operator $\mathcal{T}: \mathcal{P}(\Sigma^*) \to \mathcal{P}(\Sigma^*)$ on the Wasserstein space of distributions over token sequences. Prove convergence to fixed points by establishing contractivity of $\mathcal{T}$ in $W_2$ under appropriate conditions on the transition kernel.

2. **Key lemmas to establish:**
   - (L1) The CoT operator $\mathcal{T}$ is well-defined on $\mathcal{P}_2(\Sigma^*)$ and preserves finite second moments.
   - (L2) Spectral decomposition of $\mathcal{T}$ in a suitable function space (e.g., weighted $L^2$), relating eigenvalues to convergence rates.
   - (L3) Contractivity condition: $W_2(\mathcal{T}\mu, \mathcal{T}\nu) \leq \kappa \cdot W_2(\mu, \nu)$ for $\kappa < 1$, or weaker Lyapunov-type conditions for eventual contractivity.
   - (L4) Phase transition characterization: explicit conditions on model parameters separating power-law from exponential regimes.

3. **Potential obstacles:**
   - Token sequences form a discrete space; $W_2$ is typically defined on $\mathbb{R}^d$. Need to either embed sequences in a continuous space (e.g., via transformer hidden states) or use discrete optimal transport.
   - Non-contractivity in general: CoT operators may not be contractive globally, requiring metastability-based arguments instead.
   - The high dimensionality of token sequence space may make spectral analysis intractable without dimensionality reduction (cf. rank-40 projection in Carson & Reisizadeh).

4. **Computational support:** Use SymPy for symbolic analysis of spectral properties of simple transition operators; NumPy/SciPy for numerical eigenvalue computation and simulation of toy Markov chains; NetworkX for graph structure of transition kernels.
