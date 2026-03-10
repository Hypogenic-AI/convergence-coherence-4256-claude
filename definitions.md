# Definitions and Notation

## State Space

**Definition 1 (Reasoning State Space).** Let S = {s₁, s₂, ..., s_N} be a finite set of *reasoning states*, representing distinct configurations of an LLM's internal representation during chain-of-thought reasoning. Each state sᵢ corresponds to a point in the embedding space ℝᵈ obtained by projecting the LLM's hidden state at a reasoning step boundary.

**Definition 2 (Metric on S).** We equip S with a metric d: S × S → ℝ≥₀ induced by the Euclidean distance on embeddings: d(sᵢ, sⱼ) = ‖eᵢ - eⱼ‖₂ where eᵢ ∈ ℝᵈ is the embedding of sᵢ.

## Probability Measures and Wasserstein Distance

**Definition 3 (Probability Simplex).** Let P(S) = {μ ∈ ℝᴺ : μᵢ ≥ 0, Σᵢ μᵢ = 1} denote the set of probability measures on S. For p ≥ 1, all measures on finite S have finite p-th moments.

**Definition 4 (Wasserstein-p Distance on P(S)).** For μ, ν ∈ P(S), the Wasserstein-p distance is:

W_p(μ, ν) = (min_{π ∈ Π(μ,ν)} Σᵢ,ⱼ πᵢⱼ · d(sᵢ, sⱼ)^p)^{1/p}

where Π(μ,ν) = {π ∈ ℝ^{N×N}≥₀ : Σⱼ πᵢⱼ = μᵢ, Σᵢ πᵢⱼ = νⱼ} is the set of couplings.

**Remark.** On finite S, W_p is always well-defined and (P(S), W_p) is a compact metric space.

## Transition Operator

**Definition 5 (CoT Transition Kernel).** A CoT transition kernel is a row-stochastic matrix P ∈ ℝ^{N×N} where Pᵢⱼ = P(X_{t+1} = sⱼ | X_t = sᵢ) represents the probability of transitioning from reasoning state sᵢ to sⱼ in one CoT step.

**Definition 6 (CoT Transition Operator).** The CoT transition operator T: P(S) → P(S) is defined by (Tμ)ⱼ = Σᵢ μᵢ Pᵢⱼ, i.e., Tμ = μP in row-vector notation. This maps the current distribution over reasoning states to the distribution after one reasoning step.

## Contraction and Mixing Coefficients

**Definition 7 (Dobrushin Coefficient).** The Dobrushin (ergodicity) coefficient of a transition matrix P is:

δ(P) = (1/2) max_{i,k} Σⱼ |Pᵢⱼ - Pₖⱼ| = 1 - min_{i,k} Σⱼ min(Pᵢⱼ, Pₖⱼ)

It satisfies δ(P) ∈ [0, 1], with δ(P) < 1 iff P has a positive column.

**Definition 8 (Spectral Gap).** For an irreducible, aperiodic transition matrix P with stationary distribution π, the spectral gap is γ = 1 - |λ₂|, where λ₂ is the second-largest eigenvalue of P in absolute value. We have 1 = λ₁ ≥ |λ₂| ≥ ... ≥ |λ_N|.

## Metastable Structure

**Definition 9 (K-Cluster Metastable Structure).** A transition matrix P has (K, ε)-metastable structure if S can be partitioned into clusters C₁, ..., C_K such that:
- Within-cluster transition probabilities: Pᵢⱼ = Θ(1/|C_k|) for sᵢ, sⱼ ∈ C_k
- Between-cluster transition probabilities: Pᵢⱼ = O(ε/N) for sᵢ ∈ C_k, sⱼ ∈ C_l, k ≠ l
- ε ≪ 1 controls the inter-cluster coupling strength

**Definition 10 (Solution Fixed Point).** A probability measure μ* ∈ P(S) is a fixed point of T if Tμ* = μ*. This corresponds to a stationary distribution of the Markov chain with kernel P. We call μ* a *solution fixed point* if it concentrates on states representing correct reasoning outcomes.
