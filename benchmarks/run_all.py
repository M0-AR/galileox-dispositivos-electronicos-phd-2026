"""Run every benchmark + live-market check, write JSON + markdown report."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
from galileox_phd.benchmarks import run_all, summary
from galileox_phd.market import verify_market

OUT = os.path.dirname(os.path.abspath(__file__))
res = run_all()
s = summary(res)
mkt = verify_market()


def _clean(o):
    try:
        import numpy as np
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
    except Exception:
        pass
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


res, s, mkt = _clean(res), _clean(s), _clean(mkt)
report = {"benchmarks": res, "summary": s, "market": mkt}
with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(report, f, indent=2)
lines = ["# Benchmark report", "", f"Passed {s['passed']}/{s['total']}", ""]
for r in res:
    mark = "PASS" if r["passed"] else "FAIL"
    lines.append(f"- [{mark}] {r['name']}: pred={r['predicted']:.5g} ref={r['reference']:.5g} err={r['rel_err']:.3%}")
lines += ["", f"market live={mkt.get('live')} quotes={list(mkt.get('quotes', {}).keys())}"]
with open(os.path.join(OUT, "REPORT.md"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
if s["failed"]:
    sys.exit(1)
