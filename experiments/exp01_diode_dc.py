"""EXP-01 Diodes in DC (Leccion 1a): Shockley + load-line vs 1N4007 datasheet."""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from galileox_phd.devices import shockley_diode, diode_dynamic_resistance

OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "../figures/exp01_diode_iv.png")
CSV = os.path.join(OUT, "../benchmarks/exp01_iv.csv")

Is, n = 3e-12, 1.15
V = np.linspace(-0.5, 1.0, 400)
I = shockley_diode(V, Is=Is, n=n)
# datasheet anchor points (1N4007 typical 25C)
anchors = [(0.60, 0.01), (0.70, 0.10), (0.95, 1.0)]

os.makedirs(os.path.dirname(CSV), exist_ok=True)
with open(CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["V_V", "I_A"])
    for v, i in zip(V, I):
        if i > 0:
            w.writerow([f"{v:.4f}", f"{float(i):.6e}"])

plt.figure(figsize=(7, 4.5))
plt.semilogy(V[V > 0], np.maximum(I[V > 0], 1e-12))
for vf, iref in anchors:
    plt.scatter([vf], [iref], s=60, zorder=5)
    plt.text(vf + 0.02, iref * 1.3, f"{vf}V@{iref}A")
plt.xlabel("V (V)"); plt.ylabel("I (A, log)")
plt.title("EXP-01 Shockley (Is=3e-12, n=1.15) vs 1N4007 anchors")
plt.grid(True, which="both", alpha=0.3)
plt.savefig(FIG, dpi=150, bbox_inches="tight")
print(f"rd@10mA={diode_dynamic_resistance(0.01, n=n):.2f} ohm")
print(f"saved {FIG} {CSV}")
