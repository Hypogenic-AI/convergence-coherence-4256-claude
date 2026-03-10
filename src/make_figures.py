"""Generate all figures for the convergence rate analysis."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "results"
FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

with open(os.path.join(RESULTS_DIR, "all_results.json")) as f:
    R = json.load(f)


# Figure 1: Exponential convergence in contractive regime
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

for key in sorted(R["exp1_contractive"].keys()):
    data = R["exp1_contractive"][key]
    w2 = data["w2_distances"]
    alpha = key.split("=")[1]
    ax1.semilogy(range(len(w2)), w2, label=f"α={alpha}", linewidth=2)

ax1.set_xlabel("Iteration n", fontsize=12)
ax1.set_ylabel("W₂(T^n μ₀, μ*)", fontsize=12)
ax1.set_title("(a) W₂ Convergence: Contractive Regime", fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Predicted vs empirical rates
alphas = []
predicted = []
empirical = []
for key in sorted(R["exp1_contractive"].keys()):
    data = R["exp1_contractive"][key]
    alphas.append(float(key.split("=")[1]))
    predicted.append(data["predicted_rate_dobrushin"])
    empirical.append(data["empirical_rate"])

ax2.plot(alphas, predicted, 'o-', label="Predicted (1-α)", linewidth=2, markersize=8)
ax2.plot(alphas, empirical, 's-', label="Empirical rate", linewidth=2, markersize=8)
ax2.plot([0, 1], [1, 0], '--', color='gray', alpha=0.5, label="y = 1-x")
ax2.set_xlabel("Mixing parameter α", fontsize=12)
ax2.set_ylabel("Convergence rate", fontsize=12)
ax2.set_title("(b) Predicted vs Empirical Rates", fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig1_contractive_convergence.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")


# Figure 2: Spectral gap vs convergence rate
fig, ax = plt.subplots(1, 1, figsize=(7, 6))

sg = R["exp4_spectral_gap"]["spectral_gaps"]
er = R["exp4_spectral_gap"]["empirical_rates"]
pr = R["exp4_spectral_gap"]["predicted_rates"]

ax.scatter(pr, er, c='steelblue', s=60, alpha=0.7, edgecolors='navy', zorder=5)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label="y = x (perfect prediction)")
# Fit line
coeffs = np.polyfit(pr, er, 1)
x_fit = np.linspace(0, 1, 100)
ax.plot(x_fit, np.polyval(coeffs, x_fit), 'r-', linewidth=2,
        label=f"Linear fit: y={coeffs[0]:.2f}x+{coeffs[1]:.2f}")
corr = R["exp4_spectral_gap"]["correlation_predicted_vs_empirical"]
ax.set_xlabel("Predicted rate (1 - γ)", fontsize=12)
ax.set_ylabel("Empirical W₂ convergence rate", fontsize=12)
ax.set_title(f"Spectral Gap vs W₂ Convergence Rate (r = {corr:.3f})", fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig2_spectral_gap_correlation.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")


# Figure 3: Metastable regime - spectral gap vs epsilon
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

eps_list = []
gaps = []
rates = []
for key in sorted(R["exp2_metastable"].keys()):
    data = R["exp2_metastable"][key]
    eps_list.append(data["epsilon"])
    gaps.append(data["spectral_gap"])
    rates.append(data["exp_fit_rate"])

ax1.loglog(eps_list, gaps, 'o-', linewidth=2, markersize=8, color='steelblue')
# Fit power law
log_eps = np.log(eps_list)
log_gaps = np.log(gaps)
coeffs = np.polyfit(log_eps, log_gaps, 1)
ax1.loglog(eps_list, np.exp(np.polyval(coeffs, log_eps)), '--', color='red',
           label=f"γ ∝ ε^{coeffs[0]:.2f}")
ax1.set_xlabel("Inter-cluster coupling ε", fontsize=12)
ax1.set_ylabel("Spectral gap γ", fontsize=12)
ax1.set_title("(a) Spectral Gap vs Coupling Strength", fontsize=13)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

ax2.plot(eps_list, rates, 'o-', linewidth=2, markersize=8, color='steelblue')
ax2.plot(eps_list, [1 - g for g in gaps], 's--', linewidth=2, markersize=8, color='red',
         label="Predicted (1-γ)")
ax2.set_xlabel("Inter-cluster coupling ε", fontsize=12)
ax2.set_ylabel("Convergence rate", fontsize=12)
ax2.set_title("(b) Convergence Rate vs Coupling", fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig3_metastable_regime.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")


# Figure 4: Phase transition
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

pt = R["exp3_phase_transition"]
eps_arr = np.array(pt["epsilons"])
exp_r2 = np.array(pt["exp_r2s"])
pow_r2 = np.array(pt["pow_r2s"])
sg_arr = np.array(pt["spectral_gaps"])

ax1.semilogx(eps_arr, exp_r2, 'o-', label="Exponential R²", linewidth=2, markersize=5, color='steelblue')
ax1.semilogx(eps_arr, pow_r2, 's-', label="Power-law R²", linewidth=2, markersize=5, color='coral')
ax1.axvline(pt["transition_epsilon"], color='gray', linestyle='--', alpha=0.7,
            label=f"Crossover ε≈{pt['transition_epsilon']:.3f}")
ax1.set_xlabel("Inter-cluster coupling ε", fontsize=12)
ax1.set_ylabel("R² (goodness of fit)", fontsize=12)
ax1.set_title("(a) Exponential vs Power-Law Fit Quality", fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

ax2.semilogx(eps_arr, sg_arr, 'o-', linewidth=2, markersize=5, color='steelblue')
ax2.set_xlabel("Inter-cluster coupling ε", fontsize=12)
ax2.set_ylabel("Spectral gap γ", fontsize=12)
ax2.set_title("(b) Spectral Gap vs Coupling", fontsize=13)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig4_phase_transition.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")


# Figure 5: Bifurcation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

couplings = []
final_w2 = []
sg_bif = []
for key in sorted(R["exp5_bifurcation"].keys()):
    data = R["exp5_bifurcation"][key]
    couplings.append(data["coupling"])
    final_w2.append(data["final_w2_between"])
    sg_bif.append(data["spectral_gap"])

ax1.semilogy(couplings, [max(x, 1e-10) for x in final_w2], 'o-', linewidth=2, markersize=8, color='steelblue')
ax1.set_xlabel("Inter-basin coupling", fontsize=12)
ax1.set_ylabel("Final W₂(μ₁, μ₂)", fontsize=12)
ax1.set_title("(a) Convergence of Different Initial Conditions", fontsize=13)
ax1.grid(True, alpha=0.3)

ax2.plot(couplings, sg_bif, 'o-', linewidth=2, markersize=8, color='steelblue')
ax2.set_xlabel("Inter-basin coupling", fontsize=12)
ax2.set_ylabel("Spectral gap γ", fontsize=12)
ax2.set_title("(b) Spectral Gap vs Coupling (Bistable)", fontsize=13)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig5_bifurcation.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved.")


# Figure 6: Complexity scaling
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

data = R["exp6_complexity"]
K_vals = data["K_values"]
sg_vals = data["spectral_gaps"]
mt_vals = data["mixing_times"]

ax1.plot(K_vals, sg_vals, 'o-', linewidth=2, markersize=8, color='steelblue')
ax1.plot(K_vals, [0.05/k * (k+1) for k in K_vals], 's--', color='red',
         label="γ ≈ ε(K+1)/K²·M", alpha=0.7)
ax1.set_xlabel("Number of clusters K", fontsize=12)
ax1.set_ylabel("Spectral gap γ", fontsize=12)
ax1.set_title("(a) Spectral Gap vs Problem Complexity", fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

ax2.plot(K_vals, mt_vals, 'o-', linewidth=2, markersize=8, color='steelblue')
ax2.set_xlabel("Number of clusters K", fontsize=12)
ax2.set_ylabel("Mixing time (1/e threshold)", fontsize=12)
ax2.set_title("(b) Mixing Time vs Complexity", fontsize=13)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig6_complexity_scaling.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

print("\nAll figures generated successfully.")
