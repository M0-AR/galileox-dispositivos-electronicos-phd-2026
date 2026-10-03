"""EXP-02 Rectifiers + multipliers in AC (Leccion 1b)."""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from galileox_phd.devices import half_wave_dc, full_wave_bridge_dc, capacitor_ripple, voltage_multiplier_out

OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "../figures/exp02_rectifiers.png")
CSV = os.path.join(OUT, "../benchmarks/exp02_rectifiers.csv")

f = 60.0
t = np.linspace(0, 2 / f, 1000)
Vsec = 12 * np.sqrt(2) * np.sin(2 * np.pi * f * t)  # 12 Vrms secondary
Vd = 0.7
half = np.maximum(Vsec - Vd, 0)
bridge = np.abs(Vsec) - Vd
bridge = np.maximum(bridge, 0)

Vp = 12 * np.sqrt(2)
rows = [
    ("half_wave_Vdc", half_wave_dc(Vp)),
    ("bridge_Vdc", full_wave_bridge_dc(Vp)),
    ("ripple_half_0.5A_1000uF", capacitor_ripple(0.5, 1000e-6, f, False)),
    ("ripple_full_0.5A_1000uF", capacitor_ripple(0.5, 1000e-6, f, True)),
    ("doubler_12Vpk", voltage_multiplier_out(Vp, 2)),
    ("tripler_12Vpk", voltage_multiplier_out(Vp, 3)),
]
os.makedirs(os.path.dirname(CSV), exist_ok=True)
with open(CSV, "w", newline="") as fcsv:
    w = csv.writer(fcsv); w.writerow(["metric", "value"])
    w.writerows(rows)
for k, v in rows:
    print(f"{k}={v:.4f}")

fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
ax[0].plot(t * 1e3, Vsec, label="secondary")
ax[0].plot(t * 1e3, half, label="half-wave out (ideal-diode)")
ax[0].legend(); ax[0].set_ylabel("V"); ax[0].grid(alpha=0.3)
ax[1].plot(t * 1e3, bridge, label="bridge out", color="tab:orange")
ax[1].set_xlabel("ms"); ax[1].set_ylabel("V"); ax[1].grid(alpha=0.3); ax[1].legend()
fig.suptitle("EXP-02 Half-wave vs bridge (12 Vrms, 60 Hz)")
fig.savefig(FIG, dpi=150, bbox_inches="tight")
print(f"saved {FIG} {CSV}")
