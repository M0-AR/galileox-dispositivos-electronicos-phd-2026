"""EXP-03 BJT as switch + inductive load (Leccion 2)."""
import csv, os
from galileox_phd.devices import bjt_fixed_bias, bjt_divider_bias
OUT = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(OUT, "../benchmarks/exp03_bjt_switch.csv")
Vcc, Rc = 12.0, 100.0  # 120 mA lamp / relay coil proxy
for beta in (100, 200, 300):
    q = bjt_fixed_bias(Vcc, Rb=10e3, Rc=Rc, beta=beta)
    print(f"fixed beta={beta}: Ib={q['Ib']*1e3:.2f}mA Ic={q['Ic']*1e3:.1f}mA Vce={q['Vce']:.2f} {q['mode']}")
print("--- divider (stable) ---")
for beta in (100, 200, 300):
    q = bjt_divider_bias(12, 47e3, 10e3, Rc=1e3, Re=470, beta=beta)
    print(f"divider beta={beta}: Ic={q['Ic']*1e3:.2f}mA Vce={q['Vce']:.2f} {q['mode']}")
# flyback diode note: energy 1/2 L I^2 must circulate; record design rule
os.makedirs(os.path.dirname(CSV), exist_ok=True)
with open(CSV, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["beta", "Ib_mA_fixed", "Ic_mA_fixed", "mode_fixed"])
    for beta in (100, 150, 200, 250, 300):
        q = bjt_fixed_bias(Vcc, 10e3, Rc, beta)
        w.writerow([beta, f"{q['Ib']*1e3:.3f}", f"{q['Ic']*1e3:.2f}", q["mode"]])
print(f"saved {CSV} | rule: always add 1N4007 flyback across inductive load")
