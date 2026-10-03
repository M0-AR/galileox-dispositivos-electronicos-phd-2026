import math
from galileox_phd.benchmarks import run_all, summary
from galileox_phd.devices import triac_power_fraction, full_wave_bridge_dc, half_wave_dc


def test_all_benchmarks_pass():
    res = run_all()
    bad = [r for r in res if not r["passed"]]
    assert not bad, f"failed: {bad}"


def test_triac_symmetry_anchor():
    assert abs(triac_power_fraction(math.pi / 2) - 0.5) < 1e-9


def test_bridge_identity_ideal():
    Vp = 15.0
    assert abs(full_wave_bridge_dc(Vp, Vd=0.0) - 2 * half_wave_dc(Vp, Vd=0.0)) < 1e-9
