"""EXP-04 BJT small-signal amplifiers (Leccion 3): re-model + fixed vs divider."""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from galileox_phd.devices import bjt_divider_bias, re_model_gain
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "../figures/exp04_gain_vs_Ie.png")
CSV = os.path.join(OUT, "../benchmarks/exp04_gain.csv")

Ie = np.logspace(-4, -2, 60)  # 0.1..10 mA
Av_bypass = [re_model_gain(2200, 0.0, i)["Av"] for i in Ie]
Av_unbypass = [re_model_gain(2200, 470.0, i)["Av"] for i in Ie]
q = bjt_divider_bias(12, 47e3, 10e3, Rc=2200, Re=470, beta=180)
print(f"Q-point: Ic={q['Ic']*1e3:.2f}mA Vce={q['Vce']:.2f}V")
print(f"Av bypassed@1mA={re_model_gain(2200,0,1e-3)['Av']:.1f} unbypassed={re_model_gain(2200,470,1e-3)['Av']:.2f}")
os.makedirs(os.path.dirname(CSV), exist_ok=True)
with open(CSV, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Ie_A", "Av_bypassed", "Av_Re470"])
    for i, a, b in zip(Ie, Av_bypass, Av_unbypass):
        w.writerow([f"{i:.6e}", f"{a:.3f}", f"{b:.3f}"])
plt.figure(figsize=(7, 4.5))
plt.semilogx(Ie * 1e3, np.abs(Av_bypass), label="bypassed (Av=Rc/re)")
plt.semilogx(Ie * 1e3, np.abs(Av_unbypass), label="unbypassed Re=470")
plt.xlabel("Ie (mA)"); plt.ylabel("|Av|"); plt.grid(True, which="both", alpha=0.3); plt.legend()
plt.title("EXP-04 Hidden pattern: |Av| scales linearly with Ie when bypassed")
plt.savefig(FIG, dpi=150, bbox_inches="tight")
print(f"saved {FIG} {CSV}")
