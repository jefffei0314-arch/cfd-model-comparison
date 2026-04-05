import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# Load data
# =========================
exp = pd.read_csv("experiment.csv")
sim = pd.read_csv("simulation.csv")

# Sort data
exp = exp.sort_values("time")
sim = sim.sort_values("time")

# =========================
# Create 3 "models" (temporary)
# =========================
sim1 = sim.copy()  # Bingham
sim2 = sim.copy()  # Quadratic
sim3 = sim.copy()  # Turbulence

sim1 = pd.read_csv("simulation_bingham.csv")
sim2 = pd.read_csv("simulation_quadratic.csv")
sim3 = pd.read_csv("simulation_turbulence.csv")

# =========================
# Interpolation
# =========================
def interpolate(sim_data):
    return np.interp(exp["time"], sim_data["time"], sim_data["velocity"])

sim1_interp = interpolate(sim1)
sim2_interp = interpolate(sim2)
sim3_interp = interpolate(sim3)

# =========================
# Error + RMSE
# =========================
def compute_rmse(sim_interp):
    error = abs(exp["velocity"] - sim_interp)
    rmse = np.sqrt(np.mean(error**2))
    return rmse

rmse1 = compute_rmse(sim1_interp)
rmse2 = compute_rmse(sim2_interp)
rmse3 = compute_rmse(sim3_interp)

print(f"Bingham RMSE: {rmse1:.2f}")
print(f"Quadratic RMSE: {rmse2:.2f}")
print(f"Turbulence RMSE: {rmse3:.2f}")

# =========================
# Find best model
# =========================
rmse_dict = {
    "Bingham": rmse1,
    "Quadratic": rmse2,
    "Turbulence": rmse3
}

best_model = min(rmse_dict, key=rmse_dict.get)
print(f"\nBest Model: {best_model}")

# =========================
# Plot
# =========================
plt.figure(figsize=(8, 5))

# Experimental
plt.plot(exp["time"], exp["velocity"], marker="o", label="Experiment")

# Models
plt.plot(exp["time"], sim1_interp, linestyle="--", label="Bingham")
plt.plot(exp["time"], sim2_interp, linestyle="--", label="Quadratic")
plt.plot(exp["time"], sim3_interp, linestyle="--", label="Turbulence")

# Annotation
plt.text(
    0.05, 0.95,
    f"Best Model: {best_model}\nRMSE:\nBingham={rmse1:.2f}\nQuadratic={rmse2:.2f}\nTurbulence={rmse3:.2f}",
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.7)
)

plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("CFD Model Comparison and Validation")
plt.legend()
plt.grid()
plt.tight_layout()

plt.savefig("model_comparison.png", dpi=300)
plt.show()