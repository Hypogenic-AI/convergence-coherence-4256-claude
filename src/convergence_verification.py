"""
Computational verification of convergence rate theorems for CoT as discrete dynamical systems.

This script:
1. Constructs toy transition matrices modeling CoT reasoning
2. Computes spectral properties (eigenvalues, spectral gap, Dobrushin coefficient)
3. Simulates Markov chain convergence and measures W_2 decay rates
4. Verifies exponential vs power-law convergence predictions
5. Tests phase transition between convergence regimes
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.linalg import eig
import json
import os
import random

# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

RESULTS_DIR = "results"
FIGURES_DIR = "figures"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


# ============================================================
# Core Mathematical Functions
# ============================================================

def wasserstein_2(mu, nu, cost_matrix):
    """
    Compute W_2 distance between discrete distributions mu, nu
    using the cost matrix C where C[i,j] = d(s_i, s_j)^2.
    Uses linear programming via the Hungarian algorithm on a discretized coupling.
    For exact computation on small discrete spaces, we solve the OT problem.
    """
    n = len(mu)
    # Solve optimal transport via linear programming
    # For discrete measures, W_2^2 = min_{pi in Pi(mu,nu)} sum_{i,j} pi_{ij} * C_{ij}
    from scipy.optimize import linprog

    # Variables: pi_{ij} for i,j in {0,...,n-1}, flattened to n^2 variables
    c = cost_matrix.flatten()

    # Constraints: row sums = mu, col sums = nu
    # Row sum constraints: sum_j pi_{ij} = mu_i for each i
    A_eq_rows = np.zeros((n, n * n))
    for i in range(n):
        A_eq_rows[i, i * n:(i + 1) * n] = 1.0

    # Col sum constraints: sum_i pi_{ij} = nu_j for each j
    A_eq_cols = np.zeros((n, n * n))
    for j in range(n):
        A_eq_cols[j, j::n] = 1.0

    A_eq = np.vstack([A_eq_rows, A_eq_cols])
    b_eq = np.concatenate([mu, nu])

    bounds = [(0, None)] * (n * n)

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        return np.sqrt(max(result.fun, 0.0))
    else:
        # Fallback: use Sinkhorn approximation
        return wasserstein_2_sinkhorn(mu, nu, cost_matrix)


def wasserstein_2_sinkhorn(mu, nu, cost_matrix, reg=0.01, max_iter=1000):
    """Sinkhorn approximation of W_2 distance."""
    n = len(mu)
    K = np.exp(-cost_matrix / reg)
    u = np.ones(n)
    for _ in range(max_iter):
        v = nu / (K.T @ u + 1e-300)
        u = mu / (K @ v + 1e-300)
    pi = np.diag(u) @ K @ np.diag(v)
    return np.sqrt(max(np.sum(pi * cost_matrix), 0.0))


def dobrushin_coefficient(P):
    """Compute the Dobrushin ergodicity coefficient of transition matrix P."""
    n = P.shape[0]
    max_tv = 0.0
    for i in range(n):
        for k in range(i + 1, n):
            tv = 0.5 * np.sum(np.abs(P[i] - P[k]))
            max_tv = max(max_tv, tv)
    return max_tv


def spectral_gap(P):
    """Compute spectral gap gamma = 1 - |lambda_2| of transition matrix P."""
    eigenvalues = eig(P)[0]
    eigenvalues = np.sort(np.abs(eigenvalues))[::-1]
    if len(eigenvalues) < 2:
        return 1.0
    return 1.0 - eigenvalues[1]


def stationary_distribution(P):
    """Compute stationary distribution of transition matrix P."""
    eigenvalues, eigenvectors = eig(P.T)
    # Find eigenvalue closest to 1
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])
    pi = pi / np.sum(pi)
    # Ensure non-negative
    pi = np.abs(pi)
    pi = pi / np.sum(pi)
    return pi


def make_cost_matrix(embeddings):
    """Compute squared distance cost matrix from embeddings."""
    n = len(embeddings)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = np.sum((embeddings[i] - embeddings[j]) ** 2)
    return C


# ============================================================
# Experiment 1: Contractive Regime - Exponential Convergence
# ============================================================

def make_contractive_chain(n, alpha=0.3):
    """
    Create a contractive transition matrix with Dobrushin coefficient < 1.
    Uses a mixture: P = (1-alpha)*I + alpha*ones/n (lazy random walk to uniform).
    This has Dobrushin coefficient = 1 - alpha and spectral gap = alpha.
    """
    P = (1 - alpha) * np.eye(n) + alpha * np.ones((n, n)) / n
    return P


def experiment_contractive_convergence():
    """
    Verify Theorem 1: Exponential convergence under contraction.

    For a contractive operator with Dobrushin coefficient kappa,
    we expect W_2(T^n mu_0, mu*) <= kappa^n * W_2(mu_0, mu*).
    """
    print("=" * 60)
    print("EXPERIMENT 1: Contractive Regime - Exponential Convergence")
    print("=" * 60)

    N = 10  # state space size
    alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
    n_steps = 50

    # Random embeddings for state space
    embeddings = np.random.randn(N, 3)
    C = make_cost_matrix(embeddings)

    results = {}

    for alpha in alphas:
        P = make_contractive_chain(N, alpha)
        pi_star = stationary_distribution(P)
        kappa = dobrushin_coefficient(P)
        gamma = spectral_gap(P)

        # Initial distribution: point mass on state 0
        mu = np.zeros(N)
        mu[0] = 1.0

        w2_distances = []
        w2_initial = wasserstein_2(mu, pi_star, C)

        for t in range(n_steps):
            w2 = wasserstein_2(mu, pi_star, C)
            w2_distances.append(w2)
            mu = mu @ P

        # Fit exponential decay: log(W2) = log(C) + n * log(rate)
        w2_arr = np.array(w2_distances)
        positive_mask = w2_arr > 1e-15
        if np.sum(positive_mask) > 2:
            log_w2 = np.log(w2_arr[positive_mask])
            steps = np.arange(n_steps)[positive_mask]
            # Linear regression on log scale
            coeffs = np.polyfit(steps, log_w2, 1)
            empirical_rate = np.exp(coeffs[0])
        else:
            empirical_rate = 0.0

        results[f"alpha={alpha}"] = {
            "dobrushin_coefficient": float(kappa),
            "spectral_gap": float(gamma),
            "predicted_rate_dobrushin": float(1 - alpha),  # = kappa
            "predicted_rate_spectral": float(1 - gamma),
            "empirical_rate": float(empirical_rate),
            "w2_distances": [float(x) for x in w2_distances[:20]],
            "initial_w2": float(w2_initial),
        }

        print(f"\nalpha={alpha}:")
        print(f"  Dobrushin coeff (kappa) = {kappa:.4f}")
        print(f"  Spectral gap (gamma)    = {gamma:.4f}")
        print(f"  Predicted rate (1-alpha) = {1-alpha:.4f}")
        print(f"  Empirical rate           = {empirical_rate:.4f}")
        print(f"  W2 distances (first 5):  {[f'{x:.4f}' for x in w2_distances[:5]]}")

    return results


# ============================================================
# Experiment 2: Metastable Regime - Power-Law Convergence
# ============================================================

def make_metastable_chain(K, M, epsilon):
    """
    Create a transition matrix with (K, epsilon)-metastable structure.
    K clusters of size M each. Total states = K*M.
    Within-cluster: uniform mixing with rate 1/M.
    Between-cluster: transition rate epsilon/(K*M).
    """
    N = K * M
    P = np.zeros((N, N))

    for k in range(K):
        start = k * M
        end = (k + 1) * M
        # Within-cluster: uniform mixing
        for i in range(start, end):
            for j in range(start, end):
                P[i, j] = (1 - epsilon) / M
            # Between-cluster: small transitions
            for l in range(K):
                if l != k:
                    l_start = l * M
                    l_end = (l + 1) * M
                    for j in range(l_start, l_end):
                        P[i, j] = epsilon / (N - M)

    # Normalize rows
    P = P / P.sum(axis=1, keepdims=True)
    return P


def experiment_metastable_convergence():
    """
    Verify Theorem 3: Power-law convergence in metastable regime.

    With K clusters, size M, coupling epsilon, we expect convergence
    governed by inter-cluster mixing time ~ KM/epsilon.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Metastable Regime - Power-Law Convergence")
    print("=" * 60)

    K = 3  # clusters
    M = 5  # states per cluster
    epsilons = [0.01, 0.05, 0.1, 0.2, 0.5]
    n_steps = 500

    N = K * M
    # Embeddings: clusters at distance ~10 apart, within-cluster distance ~1
    embeddings = np.zeros((N, 3))
    for k in range(K):
        center = np.array([10.0 * np.cos(2 * np.pi * k / K),
                           10.0 * np.sin(2 * np.pi * k / K),
                           0.0])
        for m in range(M):
            embeddings[k * M + m] = center + np.random.randn(3) * 0.5

    C = make_cost_matrix(embeddings)

    results = {}

    for epsilon in epsilons:
        P = make_metastable_chain(K, M, epsilon)
        pi_star = stationary_distribution(P)
        kappa = dobrushin_coefficient(P)
        gamma = spectral_gap(P)

        # Get all eigenvalues
        eigenvalues = np.sort(np.abs(eig(P)[0]))[::-1]

        # Initial distribution: concentrated in cluster 0
        mu = np.zeros(N)
        mu[:M] = 1.0 / M

        w2_distances = []
        for t in range(n_steps):
            w2 = wasserstein_2(mu, pi_star, C)
            w2_distances.append(w2)
            mu = mu @ P

        # Fit both exponential and power-law
        w2_arr = np.array(w2_distances)
        positive_mask = w2_arr > 1e-12
        steps_pos = np.arange(n_steps)[positive_mask]
        w2_pos = w2_arr[positive_mask]

        if len(steps_pos) > 10:
            # Exponential fit: log(W2) = a + b*n
            log_w2 = np.log(w2_pos)
            exp_coeffs = np.polyfit(steps_pos, log_w2, 1)
            exp_rate = np.exp(exp_coeffs[0])
            exp_residuals = log_w2 - np.polyval(exp_coeffs, steps_pos)
            exp_r2 = 1 - np.var(exp_residuals) / np.var(log_w2)

            # Power-law fit: log(W2) = a + b*log(n+1)
            log_steps = np.log(steps_pos + 1)
            pow_coeffs = np.polyfit(log_steps, log_w2, 1)
            pow_exponent = pow_coeffs[0]
            pow_residuals = log_w2 - np.polyval(pow_coeffs, log_steps)
            pow_r2 = 1 - np.var(pow_residuals) / np.var(log_w2)
        else:
            exp_rate = exp_r2 = pow_exponent = pow_r2 = 0.0

        results[f"eps={epsilon}"] = {
            "K": K, "M": M, "epsilon": float(epsilon),
            "N": N,
            "dobrushin_coefficient": float(kappa),
            "spectral_gap": float(gamma),
            "top_5_eigenvalues": [float(x) for x in eigenvalues[:5]],
            "predicted_mixing_time": float(K * M / epsilon),
            "exp_fit_rate": float(exp_rate),
            "exp_fit_r2": float(exp_r2),
            "pow_fit_exponent": float(pow_exponent),
            "pow_fit_r2": float(pow_r2),
            "w2_distances_sampled": [float(w2_distances[t]) for t in [0, 5, 10, 20, 50, 100, 200, 499] if t < len(w2_distances)],
        }

        print(f"\nepsilon={epsilon}:")
        print(f"  Spectral gap         = {gamma:.6f}")
        print(f"  Dobrushin coeff      = {kappa:.4f}")
        print(f"  Top eigenvalues      = {[f'{x:.4f}' for x in eigenvalues[:5]]}")
        print(f"  Predicted mix time   = {K*M/epsilon:.1f}")
        print(f"  Exp fit: rate={exp_rate:.4f}, R²={exp_r2:.4f}")
        print(f"  Pow fit: exp={pow_exponent:.4f}, R²={pow_r2:.4f}")
        print(f"  Better fit: {'Exponential' if exp_r2 > pow_r2 else 'Power-law'}")

    return results


# ============================================================
# Experiment 3: Phase Transition Between Regimes
# ============================================================

def experiment_phase_transition():
    """
    Verify Theorem 4: Phase transition between exponential and power-law regimes.

    As inter-cluster coupling epsilon increases, the system transitions from
    metastable (power-law) to well-mixed (exponential) convergence.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Phase Transition Between Regimes")
    print("=" * 60)

    K = 3
    M = 5
    N = K * M

    # Fine grid of epsilon values
    epsilons = np.logspace(-3, 0, 30)
    n_steps = 300

    # Fixed embeddings
    embeddings = np.zeros((N, 3))
    for k in range(K):
        center = np.array([10.0 * np.cos(2 * np.pi * k / K),
                           10.0 * np.sin(2 * np.pi * k / K), 0.0])
        for m in range(M):
            embeddings[k * M + m] = center + 0.5 * np.random.randn(3)
    C = make_cost_matrix(embeddings)

    results = {"epsilons": [], "spectral_gaps": [], "dobrushin_coeffs": [],
               "exp_rates": [], "exp_r2s": [], "pow_exponents": [], "pow_r2s": [],
               "better_fit": []}

    for epsilon in epsilons:
        P = make_metastable_chain(K, M, float(epsilon))
        pi_star = stationary_distribution(P)
        gamma = spectral_gap(P)
        kappa = dobrushin_coefficient(P)

        mu = np.zeros(N)
        mu[0] = 1.0

        w2_distances = []
        for t in range(n_steps):
            w2 = wasserstein_2(mu, pi_star, C)
            w2_distances.append(w2)
            mu = mu @ P

        w2_arr = np.array(w2_distances)
        positive_mask = w2_arr > 1e-12
        steps_pos = np.arange(n_steps)[positive_mask]
        w2_pos = w2_arr[positive_mask]

        exp_rate = exp_r2 = pow_exp = pow_r2 = 0.0
        if len(steps_pos) > 10:
            log_w2 = np.log(w2_pos)

            exp_coeffs = np.polyfit(steps_pos, log_w2, 1)
            exp_rate = np.exp(exp_coeffs[0])
            exp_res = log_w2 - np.polyval(exp_coeffs, steps_pos)
            exp_r2 = 1 - np.var(exp_res) / np.var(log_w2) if np.var(log_w2) > 0 else 0

            log_steps = np.log(steps_pos + 1)
            pow_coeffs = np.polyfit(log_steps, log_w2, 1)
            pow_exp = pow_coeffs[0]
            pow_res = log_w2 - np.polyval(pow_coeffs, log_steps)
            pow_r2 = 1 - np.var(pow_res) / np.var(log_w2) if np.var(log_w2) > 0 else 0

        results["epsilons"].append(float(epsilon))
        results["spectral_gaps"].append(float(gamma))
        results["dobrushin_coeffs"].append(float(kappa))
        results["exp_rates"].append(float(exp_rate))
        results["exp_r2s"].append(float(exp_r2))
        results["pow_exponents"].append(float(pow_exp))
        results["pow_r2s"].append(float(pow_r2))
        results["better_fit"].append("exp" if exp_r2 > pow_r2 else "pow")

    # Find approximate transition point
    fit_diff = np.array(results["exp_r2s"]) - np.array(results["pow_r2s"])
    transition_idx = np.argmin(np.abs(fit_diff))
    transition_epsilon = results["epsilons"][transition_idx]

    results["transition_epsilon"] = float(transition_epsilon)
    results["transition_spectral_gap"] = float(results["spectral_gaps"][transition_idx])

    print(f"\nPhase transition at epsilon ≈ {transition_epsilon:.4f}")
    print(f"Spectral gap at transition: {results['spectral_gaps'][transition_idx]:.6f}")
    print(f"\nRegime classification:")
    for i in range(0, len(epsilons), 5):
        eps = results["epsilons"][i]
        bf = results["better_fit"][i]
        er2 = results["exp_r2s"][i]
        pr2 = results["pow_r2s"][i]
        print(f"  eps={eps:.4f}: {bf} (exp_R²={er2:.3f}, pow_R²={pr2:.3f})")

    return results


# ============================================================
# Experiment 4: Spectral Gap vs Convergence Rate
# ============================================================

def experiment_spectral_gap_relationship():
    """
    Verify the relationship between spectral gap and convergence rate.

    Theorem 2 predicts: convergence rate = |lambda_2| = 1 - gamma.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: Spectral Gap vs Convergence Rate")
    print("=" * 60)

    N = 8
    n_trials = 30
    n_steps = 100

    embeddings = np.random.randn(N, 3)
    C = make_cost_matrix(embeddings)

    results = {"spectral_gaps": [], "empirical_rates": [], "dobrushin_coeffs": [],
               "predicted_rates": []}

    for trial in range(n_trials):
        # Random transition matrix with varying mixing properties
        # Generate random stochastic matrix
        raw = np.random.exponential(1.0, (N, N))
        # Add diagonal dominance with varying strength
        diag_strength = np.random.uniform(0.1, 5.0)
        raw += diag_strength * np.eye(N)
        P = raw / raw.sum(axis=1, keepdims=True)

        pi_star = stationary_distribution(P)
        gamma = spectral_gap(P)
        kappa = dobrushin_coefficient(P)

        mu = np.zeros(N)
        mu[0] = 1.0

        w2_distances = []
        for t in range(n_steps):
            w2 = wasserstein_2(mu, pi_star, C)
            w2_distances.append(w2)
            mu = mu @ P

        w2_arr = np.array(w2_distances)
        positive_mask = w2_arr > 1e-12
        steps_pos = np.arange(n_steps)[positive_mask]
        w2_pos = w2_arr[positive_mask]

        if len(steps_pos) > 5:
            log_w2 = np.log(w2_pos)
            coeffs = np.polyfit(steps_pos, log_w2, 1)
            emp_rate = np.exp(coeffs[0])
        else:
            emp_rate = 0.0

        results["spectral_gaps"].append(float(gamma))
        results["empirical_rates"].append(float(emp_rate))
        results["dobrushin_coeffs"].append(float(kappa))
        results["predicted_rates"].append(float(1 - gamma))

    # Compute correlation
    sg = np.array(results["spectral_gaps"])
    er = np.array(results["empirical_rates"])
    pr = np.array(results["predicted_rates"])

    correlation = np.corrcoef(pr, er)[0, 1]
    results["correlation_predicted_vs_empirical"] = float(correlation)

    print(f"\nCorrelation between predicted (1-gamma) and empirical rate: {correlation:.4f}")
    print(f"\nSample results:")
    for i in range(0, min(10, n_trials)):
        print(f"  Trial {i}: gamma={sg[i]:.4f}, predicted={pr[i]:.4f}, empirical={er[i]:.4f}")

    return results


# ============================================================
# Experiment 5: Multiple Fixed Points and Bifurcation
# ============================================================

def make_bistable_chain(N_per_basin, coupling, bias=0.5):
    """
    Create a chain with two absorbing-like basins connected by weak coupling.
    Bias controls which basin is the "correct" solution.
    """
    N = 2 * N_per_basin
    P = np.zeros((N, N))

    # Basin 1: states 0..N_per_basin-1, attractor at state 0
    for i in range(N_per_basin):
        # Drift toward attractor (state 0)
        if i > 0:
            P[i, i - 1] = 0.4 * (1 - coupling)  # drift toward 0
            P[i, i] = 0.4 * (1 - coupling)       # stay
            if i < N_per_basin - 1:
                P[i, i + 1] = 0.2 * (1 - coupling)  # drift away
            else:
                P[i, i] += 0.2 * (1 - coupling)
        else:
            P[0, 0] = 0.8 * (1 - coupling)
            P[0, 1] = 0.2 * (1 - coupling)

        # Cross-basin coupling
        for j in range(N_per_basin, N):
            P[i, j] = coupling / N_per_basin

    # Basin 2: states N_per_basin..N-1, attractor at state N_per_basin
    for i in range(N_per_basin, N):
        local_i = i - N_per_basin
        if local_i > 0:
            P[i, i - 1] = 0.4 * (1 - coupling)
            P[i, i] = 0.4 * (1 - coupling)
            if local_i < N_per_basin - 1:
                P[i, i + 1] = 0.2 * (1 - coupling)
            else:
                P[i, i] += 0.2 * (1 - coupling)
        else:
            P[i, i] = 0.8 * (1 - coupling)
            if N_per_basin + 1 < N:
                P[i, i + 1] = 0.2 * (1 - coupling)
            else:
                P[i, i] += 0.2 * (1 - coupling)

        for j in range(N_per_basin):
            P[i, j] = coupling / N_per_basin

    # Normalize
    P = P / P.sum(axis=1, keepdims=True)
    return P


def experiment_bifurcation():
    """
    Investigate bifurcation: how convergence to different fixed points
    depends on initial conditions and coupling strength.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 5: Bifurcation and Multiple Attractors")
    print("=" * 60)

    N_per = 5
    N = 2 * N_per
    n_steps = 200

    embeddings = np.zeros((N, 2))
    for i in range(N_per):
        embeddings[i] = [-5.0 + i * 0.5, 0.0]
        embeddings[N_per + i] = [5.0 - i * 0.5, 0.0]
    C = make_cost_matrix(embeddings)

    couplings = [0.001, 0.01, 0.05, 0.1, 0.3, 0.5]
    results = {}

    for coupling in couplings:
        P = make_bistable_chain(N_per, coupling)
        pi_star = stationary_distribution(P)
        gamma = spectral_gap(P)
        eigenvalues = np.sort(np.abs(eig(P)[0]))[::-1]

        # Test convergence from two initial conditions
        # IC1: start in basin 1
        mu1 = np.zeros(N)
        mu1[0] = 1.0

        # IC2: start in basin 2
        mu2 = np.zeros(N)
        mu2[N_per] = 1.0

        w2_basin1 = []
        w2_basin2 = []
        w2_between = []

        for t in range(n_steps):
            w2_basin1.append(wasserstein_2(mu1, pi_star, C))
            w2_basin2.append(wasserstein_2(mu2, pi_star, C))
            w2_between.append(wasserstein_2(mu1, mu2, C))
            mu1 = mu1 @ P
            mu2 = mu2 @ P

        results[f"coupling={coupling}"] = {
            "coupling": float(coupling),
            "spectral_gap": float(gamma),
            "eigenvalue_gap_ratio": float(eigenvalues[1] / eigenvalues[2]) if eigenvalues[2] > 1e-10 else float('inf'),
            "top_eigenvalues": [float(x) for x in eigenvalues[:5]],
            "final_w2_basin1": float(w2_basin1[-1]),
            "final_w2_basin2": float(w2_basin2[-1]),
            "final_w2_between": float(w2_between[-1]),
            "convergence_basin1": [float(w2_basin1[t]) for t in [0, 10, 50, 100, 199]],
            "convergence_basin2": [float(w2_basin2[t]) for t in [0, 10, 50, 100, 199]],
        }

        print(f"\ncoupling={coupling}:")
        print(f"  Spectral gap: {gamma:.6f}")
        print(f"  Top eigenvalues: {[f'{x:.4f}' for x in eigenvalues[:4]]}")
        print(f"  Final W2 (basin1→π*): {w2_basin1[-1]:.6f}")
        print(f"  Final W2 (basin2→π*): {w2_basin2[-1]:.6f}")
        print(f"  Final W2 (μ1 vs μ2):  {w2_between[-1]:.6f}")

    return results


# ============================================================
# Experiment 6: Complexity vs Convergence Rate
# ============================================================

def experiment_complexity_convergence():
    """
    Analyze how problem complexity (K clusters = reasoning depth)
    affects convergence rates.
    """
    print("\n" + "=" * 60)
    print("EXPERIMENT 6: Complexity (K) vs Convergence Rate")
    print("=" * 60)

    M = 4  # fixed cluster size
    epsilon = 0.05  # fixed coupling
    K_values = [2, 3, 4, 5, 6, 8]
    n_steps = 500

    results = {"K_values": [], "spectral_gaps": [], "mixing_times": [],
               "empirical_rates": [], "predicted_mixing_times": []}

    for K in K_values:
        N = K * M
        P = make_metastable_chain(K, M, epsilon)

        embeddings = np.zeros((N, 3))
        for k in range(K):
            center = 10.0 * np.array([np.cos(2*np.pi*k/K), np.sin(2*np.pi*k/K), 0])
            for m in range(M):
                embeddings[k*M + m] = center + 0.3 * np.random.randn(3)
        C = make_cost_matrix(embeddings)

        pi_star = stationary_distribution(P)
        gamma = spectral_gap(P)

        mu = np.zeros(N)
        mu[0] = 1.0

        w2_distances = []
        for t in range(n_steps):
            w2 = wasserstein_2(mu, pi_star, C)
            w2_distances.append(w2)
            mu = mu @ P

        # Find mixing time (time to reach 1/e of initial W2)
        w2_arr = np.array(w2_distances)
        threshold = w2_arr[0] / np.e
        mixing_time = n_steps
        for t in range(n_steps):
            if w2_arr[t] < threshold:
                mixing_time = t
                break

        # Empirical rate
        positive_mask = w2_arr > 1e-12
        steps_pos = np.arange(n_steps)[positive_mask]
        if len(steps_pos) > 5:
            log_w2 = np.log(w2_arr[positive_mask])
            coeffs = np.polyfit(steps_pos, log_w2, 1)
            emp_rate = np.exp(coeffs[0])
        else:
            emp_rate = 0.0

        results["K_values"].append(K)
        results["spectral_gaps"].append(float(gamma))
        results["mixing_times"].append(int(mixing_time))
        results["empirical_rates"].append(float(emp_rate))
        results["predicted_mixing_times"].append(float(K * M / epsilon))

        print(f"\nK={K} (N={N}):")
        print(f"  Spectral gap:           {gamma:.6f}")
        print(f"  Mixing time (empirical): {mixing_time}")
        print(f"  Mixing time (predicted): {K*M/epsilon:.0f}")
        print(f"  Empirical rate:          {emp_rate:.4f}")

    # Check linear scaling of mixing time with K
    K_arr = np.array(results["K_values"], dtype=float)
    mt_arr = np.array(results["mixing_times"], dtype=float)
    if len(K_arr) > 2:
        coeffs = np.polyfit(K_arr, mt_arr, 1)
        results["mixing_time_slope"] = float(coeffs[0])
        results["mixing_time_intercept"] = float(coeffs[1])
        r2 = 1 - np.var(mt_arr - np.polyval(coeffs, K_arr)) / np.var(mt_arr)
        results["mixing_time_linear_r2"] = float(r2)
        print(f"\nMixing time ~ {coeffs[0]:.1f}*K + {coeffs[1]:.1f} (R²={r2:.3f})")

    return results


# ============================================================
# Main Execution
# ============================================================

if __name__ == "__main__":
    print("Convergence Rate Verification for CoT as Discrete Dynamical Systems")
    print("=" * 70)

    all_results = {}

    # Run all experiments
    all_results["exp1_contractive"] = experiment_contractive_convergence()
    all_results["exp2_metastable"] = experiment_metastable_convergence()
    all_results["exp3_phase_transition"] = experiment_phase_transition()
    all_results["exp4_spectral_gap"] = experiment_spectral_gap_relationship()
    all_results["exp5_bifurcation"] = experiment_bifurcation()
    all_results["exp6_complexity"] = experiment_complexity_convergence()

    # Save all results
    with open(os.path.join(RESULTS_DIR, "all_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "=" * 70)
    print("All experiments complete. Results saved to results/all_results.json")
