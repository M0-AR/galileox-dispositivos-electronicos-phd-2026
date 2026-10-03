# PAPER DRAFT — Verifying an Introductory Power-Semiconductor Syllabus End-to-End
## From Shockley to TRIAC dimmers: closed-form models, public-datasheet benchmarks, and live-market grounding

**Scope:** GalileoX *Introducción a los dispositivos electrónicos* (Lecciones 1–5). **Artefact:** reproducible Python 3.12 + Docker study, 10/10 benchmarks PASS, 5 experiments, 3 pytest gates.

### 1. Introduction
Introductory electronics courses assert that a handful of equations govern commodity devices that "revolutionised the 20th century". Students rarely see those claims *falsifiably* tested. We close the loop: implement every syllabus equation, confront it with manufacturer public data, and ground industrial relevance with 2026 live-market evidence.

### 2. Related work (online research trail, Sep–Oct 2026)
- **Textbooks/basics:** Petry (IFSC) Cap.2–3 — diodes/SCR/TRIAC ideal-vs-real, commutation, snubbers; Costa (IFRN) apostila — BJT/MOSFET/IGBT/GTO taxonomy; Palma (2018) — natural vs forced commutation; UFV ELT313 — 13 thyristor families; UNICAMP Pomilio — p-n-p-n latch, IH/IL, forced-commutation obsolescence; USP e-Aulas, UFRN IMD — BJT configs, Ebers-Moll/Gummel-Poon.
- **2025–2026 frontier:** Stanojev et al., arXiv:2603.13050 (Mar 2026) — nonlinear dq-EMT thyristor-rectifier model + IEEE-39 stability; Zeng et al. (TSTE 2025, arXiv:2503.17092) — optimal TR/IGBT-R portfolio +13.78 % revenue, 3:1 TR:IGBT-R; Jiya & Gouws (Micromachines 2020) — Si→WBG paradigm shift; Sep-2026 news — Wise+Navitas AI-computing GaN, EU power-transistor 2026–31 SiC forecast, China SiC wafer mega-contract. Our course devices (line-commutated SCR/TRIAC, LV BJT/diode) sit at the *mature-commodity* end; WBG (SiC/GaN) is the growth end — both share the same P-N physics.
- **Tooling best practice:** PySpice/ngspice (Fabrice Salvaire, GPLv3) — scriptable, versionable, CI-friendly vs GUI; SpiceXplorer/Chipify — YAML spec-driven sweeps; ROHM SPICE guide — Shockley+Rs compact models; diode-fitting calculators — extract (Is, Rs, N) from ≥3 I-V points. We adopt the *lightweight* rung: NumPy closed-forms (no simulator install) with an optional ngspice cross-check protocol (§5), Docker-pinned, network-optional.

### 3. Theory (one page)
`Vt=kT/q`; Shockley `I=Is(e^{V/nVt}−1)`, `rd=nVt/Id`; half-wave `(Vp−Vd)/π`; bridge `2Vp/π−2Vd/π`; `Vr=I/(fr·C)`; Cockcroft-Walton `N(Vp−Vd)`; BJT `Ic=βIb`, divider Thevenin `Vth,Rth`, `Ib=(Vth−Vbe)/(Rth+(β+1)Re)`, `re=Vt/Ie`, `Av=−Rc/re`; SCR half-wave `Vmax(1+cosα)/2π`, full bridge `2Vmax cosα/π`; TRIAC `P/Pmax=1−α/π+sin2α/2π`; Vf tempco −2 mV/K. Assumptions: 300 K, Si Vd 0.7 V, 60 Hz, resistive load, lumped Rs neglected except where noted.

### 4. Methods & verification protocol
- **Ground truth:** `data/datasheets/ground_truth.csv` (1N4007 Vf triple, 2N2222 hFE/VceSat, BT136 Vtm/Igt/Ih) — typical-curve values, not guaranteed min/max.
- **Benchmarks B1–B8** (`src/galileox_phd/benchmarks.py`): B1 Shockley triple (tol 25 %); B2 bridge=2×half identity; B3 ripple halving; B4 divider≫fixed stability; B5 re-gain −77±25 %; B6 SCR α=0 recovery; B7–B8 TRIAC endpoints + 90° half-power (tol 5 % identities). Runner writes `benchmarks/results.json` + `REPORT.md`, exits non-zero on FAIL.
- **Experiments EXP-01…05** regenerate every figure/CSV from scratch (Agg backend, fixed seeds — no RNG in fact).
- **Live-market layer** (`market.py`): Yahoo v8 STM/ON/IFX.DE 5-day closes; cached 2026-09-30 fallback with `live:false`. Physics CI never touches network.
- **Reproduction:** `docker compose up --build` or `pip install -r requirements.txt; PYTHONPATH=src pytest -q`.

### 5. Results
10/10 PASS (see REPORT.md). Key numbers: rd@10 mA ≈2.9 Ω; bridge 10.48 V vs half 5.16 V @12 Vrms (Vp≈17 V); ripple 4.17→2.08 V; divider ΔIc ≈15–30 % vs fixed ≈200 % over β 100→300; Av≈−85 bypassed vs −4.4 with Re=470 @1 mA; SCR 3.18→0 V over α 0→π; TRIAC 1→0.5→0. Figures in `figures/`.

### Hidden patterns (contribution)
P1 ripple-topology invariant; P2 gain-current linearity; P3 dimmer asymmetry (quantified max defect); P4 stability hierarchy; P5 unified −2 mV/K P-N thermometer. See README §2. Each is a one-line equation + plot + design rule (e.g. "double C or go bridge — same ripple, different cost").

### 6. Threats & limits
Room-temp closed forms; no trr/Qrr, no thermal runaway, no inductive-phase shift, no EMI/harmonics measurement; single-(Is,n) misfit at high injection (needs Rs); distributor prices are ranges; live quotes indicative only. Optional ngspice cross-check (not run in CI): 1N4007 default model vs Shockley overlay; Ebers-Moll vs β-model at Vce>0.5 V; SCR behavioural source vs α-law — expect <10 % agreement in DC/low-f.

### 7. Future work → PhD directions
(a) Rs-extended extraction (Is,n,Rs) from measured I-V + temperature chamber; (b) Qrr-aware rectifier loss vs WBG diodes; (c) closed-loop dimmer linearisation + THD measurement; (d) β-aware bias optimiser; (e) Si vs SiC cost-per-amp 2026–27 panel study extending §market.

### References
Rashid, *Power Electronics* 4e (Pearson 2014); Boylestad & Nashelsky; Streetman & Banerjee; Baliga; Sze; Pomilio UNICAMP text; Petry IFSC Cap.2–3; Stanojev et al. 2026; Zeng et al. 2025; Jiya-Gouws 2020; Vishay 1N4007; ON Semi P2N2222A; WeEn BT136; ROHM diode SPICE guide; PySpice docs; GalileoX course page (edX, ES, 5 wk, Oct–Dec).
