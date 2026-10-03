"""EXP-05 Thyristors DC+AC (Leccion 4-5): SCR law + TRIAC dimmer + hidden pattern."""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from galileox_phd.devices import scr_half_wave_controlled_dc, full_bridge_controlled_dc, triac_power_fraction
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "../figures/exp05_dimmer.png")
CSV = os.path.join(OUT, "../benchmarks/exp05_dimmer.csv")

alpha = np.linspace(0, np.pi, 181)
Vmax = 10.0
scr = [scr_half_wave_controlled_dc(Vmax, a) for a in alpha]
pwr = [triac_power_fraction(a) for a in alpha]
os.makedirs(os.path.dirname(CSV), exist_ok=True)
with open(CSV, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["alpha_deg", "scr_Vdc", "triac_P_Pmax"])
    for a, s, p in zip(alpha, scr, pwr):
        w.writerow([f"{np.degrees(a):.1f}", f"{s:.5f}", f"{p:.5f}"])
# hidden pattern: P(alpha)+P(pi-alpha) = 1 - (pi-2a)/pi ... verify symmetry defect
asym = [pwr[i] + pwr[-1 - i] - 1.0 for i in range(len(alpha))]
print(f"alpha=90deg P={triac_power_fraction(np.pi/2):.4f} (expect 0.5)")
print(f"max |P(a)+P(pi-a)-1|={max(abs(np.array(asym))):.4f} -> quantifies dimmer asymmetry curve")
print(f"SCR 0deg={scr[0]:.3f}V (=Vmax/pi), 180deg={scr[-1]:.4f}V (=0)")

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(np.degrees(alpha), scr); ax[0].set_ylabel("SCR Vdc (V)"); ax[0].grid(alpha=0.3)
ax[1].plot(np.degrees(alpha), pwr, color="tab:red"); ax[1].set_xlabel("firing angle (deg)")
ax[1].set_ylabel("P/Pmax"); ax[1].grid(alpha=0.3)
fig.suptitle("EXP-05 SCR Vdc(alpha) and TRIAC dimmer P(alpha)")
fig.savefig(FIG, dpi=150, bbox_inches="tight")
print(f"saved {FIG} {CSV}")
