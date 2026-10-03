"""First-principles device models (closed form, NumPy only).

Conventions
-----------
- Voltages in V, currents in A, T in Kelvin.
- Shockley: I = Is * (exp(V/(n*Vt)) - 1), Vt = k*T/q.
- Rectifier formulae assume sinusoidal mains, ideal diodes unless
  Vd (forward drop) is subtracted explicitly — the standard
  textbook treatment used in GalileoX Leccion 1.
- BJT uses Ebers-Moll simplified to beta-model in active mode,
  Ebers-Moll exponential retained for saturation checks.
- Thyristor phase-control formulae are the classical line-commutated
  results (Rashid 2014; Pomilio UNICAMP; Petry IFSC).
"""

from __future__ import annotations

import numpy as np

K_Q = 1.380649e-23 / 1.602176634e-19  # k/q = 8.617333e-05 V/K


def thermal_voltage(T: float = 300.0) -> float:
    """Thermal voltage Vt = kT/q (≈25.85 mV at 300 K)."""
    return K_Q * T


def shockley_diode(
    V: np.ndarray | float,
    Is: float = 1e-14,
    n: float = 1.0,
    T: float = 300.0,
) -> np.ndarray | float:
    """Shockley diode I-V. Vectorised over V."""
    Vt = thermal_voltage(T)
    V = np.asarray(V, dtype=float)
    # clip exponent to avoid overflow for large V in sweeps
    arg = np.clip(V / (n * Vt), -100.0, 100.0)
    return Is * (np.exp(arg) - 1.0)


def diode_dynamic_resistance(Id: float, n: float = 1.0, T: float = 300.0) -> float:
    """Small-signal rd = n*Vt / Id."""
    return n * thermal_voltage(T) / max(Id, 1e-15)


def half_wave_dc(Vp: float, Vd: float = 0.7) -> float:
    """Half-wave average: (Vp - Vd)/pi for Vp > Vd else 0."""
    return max(Vp - Vd, 0.0) / np.pi


def full_wave_bridge_dc(Vp: float, Vd: float = 0.7) -> float:
    """Bridge average: (2*Vp)/pi minus 2 diode drops distributed.

    Standard approximation: Vdc = 2*(Vp - Vd)/pi when modelling
    one conducting drop per half-cycle equivalent, or
    2*Vp/pi - 2*Vd/pi. We use the latter explicitly.
    """
    return max(2.0 * Vp / np.pi - 2.0 * Vd / np.pi, 0.0)


def capacitor_ripple(Iload: float, C: float, f: float = 60.0, full_wave: bool = True) -> float:
    """Peak-to-peak ripple Vr ≈ I / (f_ripple * C).

    full_wave -> f_ripple = 2f ; half_wave -> f_ripple = f.
    """
    fr = 2.0 * f if full_wave else f
    return Iload / (fr * C)


def voltage_multiplier_out(Vp: float, stages: int, Vd: float = 0.7) -> float:
    """Cockcroft-Walton / Greinacher ideal: N*(Vp - Vd).

    stages = number of diode-capacitor voltage steps (e.g. doubler N=2).
    """
    return max(stages * (Vp - Vd), 0.0)


def bjt_fixed_bias(Vcc: float, Rb: float, Rc: float, beta: float, Vbe: float = 0.7):
    """Fixed-bias Q-point. Returns dict(Ib, Ic, Vce, mode)."""
    Ib = max((Vcc - Vbe) / Rb, 0.0)
    Ic = beta * Ib
    Vce = Vcc - Ic * Rc
    mode = "active" if Vce > 0.2 else "saturation"
    if Vce < 0.0:  # deep saturation clamp
        Ic = max((Vcc - 0.2) / Rc, 0.0)
        Vce = 0.2
        mode = "saturation"
    return {"Ib": Ib, "Ic": Ic, "Vce": Vce, "mode": mode}


def bjt_divider_bias(
    Vcc: float, R1: float, R2: float, Rc: float, Re: float,
    beta: float, Vbe: float = 0.7,
):
    """Voltage-divider bias with Thevenin exact solution."""
    Vth = Vcc * R2 / (R1 + R2)
    Rth = R1 * R2 / (R1 + R2)
    Ib = max((Vth - Vbe) / (Rth + (beta + 1.0) * Re), 0.0)
    Ic = beta * Ib
    Ie = (beta + 1.0) * Ib
    Vce = Vcc - Ic * Rc - Ie * Re
    mode = "active" if Vce > 0.2 else "saturation"
    return {"Vth": Vth, "Rth": Rth, "Ib": Ib, "Ic": Ic, "Ie": Ie, "Vce": Vce, "mode": mode}


def re_model_gain(Rc: float, Re_ac: float, Ie: float, T: float = 300.0, ro: float = np.inf):
    """Small-signal re-model for CE stage (bypassed or unbypassed Re).

    re = Vt/Ie ; Av = -Rc_ac / re ; Zin_base = beta*re handled by caller.
    Returns dict(re, Av).
    """
    re = thermal_voltage(T) / max(Ie, 1e-12)
    Rac = Rc if np.isinf(ro) else (Rc * ro) / (Rc + ro)
    Av = -Rac / max(Re_ac + re, 1e-12) if Re_ac > 0 else -Rac / re
    # Note: when Re_ac == 0 (fully bypassed) Av = -Rc/re.
    return {"re": re, "Av": Av}


def scr_half_wave_controlled_dc(Vmax: float, alpha_rad: float) -> float:
    """Half-wave controlled (single SCR) average: Vmax/(2pi)*(1+cos a)."""
    return Vmax / (2.0 * np.pi) * (1.0 + np.cos(alpha_rad))


def full_bridge_controlled_dc(Vmax: float, alpha_rad: float) -> float:
    """Full-wave fully-controlled bridge: (2*Vmax/pi)*cos(a)."""
    return 2.0 * Vmax / np.pi * np.cos(alpha_rad)


def triac_power_fraction(alpha_rad: float) -> float:
    """Resistive-load AC phase-control power fraction.

    P/Pmax = 1 - a/pi + sin(2a)/(2pi), a in [0, pi].
    Classical dimmer law (Leccion 5).
    """
    a = float(alpha_rad)
    if a <= 0:
        return 1.0
    if a >= np.pi:
        return 0.0
    return 1.0 - a / np.pi + np.sin(2.0 * a) / (2.0 * np.pi)


def vf_temperature(Vf_ref: float, T_ref: float, T_new: float, tempco: float = -0.002) -> float:
    """Linear Vf(T) extrapolation, tempco ≈ -2 mV/K for Si."""
    return Vf_ref + tempco * (T_new - T_ref)
