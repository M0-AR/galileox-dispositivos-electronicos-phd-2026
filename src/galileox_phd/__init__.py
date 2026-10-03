"""GalileoX electronic-devices PhD benchmark package.

Implements first-principles models for the full GalileoX syllabus:
Leccion 1 diodes DC/AC + rectifiers + multipliers,
Leccion 2 BJT in DC (switch),
Leccion 3 BJT small-signal amplifiers (re-model),
Leccion 4 thyristors in DC (SCR/Shockley/DIAC/TRIAC),
Leccion 5 thyristors in AC (dimmers / phase control).

All models are closed-form / vectorised NumPy so the whole
benchmark runs without ngspice (optional cross-check only).
References are listed in docs/PAPER_DRAFT.md.
"""

from .devices import (
    thermal_voltage,
    shockley_diode,
    diode_dynamic_resistance,
    half_wave_dc,
    full_wave_bridge_dc,
    capacitor_ripple,
    voltage_multiplier_out,
    bjt_fixed_bias,
    bjt_divider_bias,
    re_model_gain,
    scr_half_wave_controlled_dc,
    full_bridge_controlled_dc,
    triac_power_fraction,
    vf_temperature,
)

__all__ = [
    "thermal_voltage",
    "shockley_diode",
    "diode_dynamic_resistance",
    "half_wave_dc",
    "full_wave_bridge_dc",
    "capacitor_ripple",
    "voltage_multiplier_out",
    "bjt_fixed_bias",
    "bjt_divider_bias",
    "re_model_gain",
    "scr_half_wave_controlled_dc",
    "full_bridge_controlled_dc",
    "triac_power_fraction",
    "vf_temperature",
]

__version__ = "1.0.0"
