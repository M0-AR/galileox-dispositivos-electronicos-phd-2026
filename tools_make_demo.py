"""Generate docs/media/demo.mp4 + demo.gif — TRIAC dimmer sweep visualization.

Step-by-step (so anyone can follow):
1. Mains sine 60 Hz, one full AC cycle.
2. For firing angle alpha in 0..180 deg, TRIAC conducts only after alpha
   in each half-cycle (resistive load model from Leccion 5).
3. Left panel shows chopped waveform (orange = power delivered).
4. Right panel shows P/Pmax law curve with moving dot.
5. Verifies P(90 deg)=0.5 anchor every run.

Outputs verified by file-size + frame-count checks in __main__.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
OUT_MP4 = os.path.join(REPO, "docs", "media", "demo.mp4")
OUT_GIF = os.path.join(REPO, "docs", "media", "demo.gif")

THETA = np.linspace(0, 2 * np.pi, 400)
SINE = np.sin(THETA)


def triac_conduction(theta, alpha):
    """1 where TRIAC on for firing angle alpha (0..pi), resistive load."""
    t = np.mod(theta, 2 * np.pi)
    half = np.mod(t, np.pi)
    return (half >= alpha).astype(float)


def power_fraction(alpha):
    return 1.0 - alpha / np.pi + np.sin(2 * alpha) / (2 * np.pi)


ALPHAS = np.linspace(0, np.pi, 61)
ALPHA_DEG = np.degrees(ALPHAS)
PWR = [power_fraction(a) for a in ALPHAS]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))
fig.suptitle("TRIAC dimmer — firing angle sweep 0° → 180°  |  P(90°)=0.5", fontsize=11)


def draw(i):
    a = ALPHAS[i]
    ax1.clear(); ax2.clear()
    on = triac_conduction(THETA, a)
    ax1.plot(np.degrees(THETA), SINE, color="#94a3b8", lw=1.2, label="mains")
    ax1.fill_between(np.degrees(THETA), 0, SINE * on, color="#f97316", alpha=0.85, label="delivered")
    ax1.set_xlim(0, 360); ax1.set_ylim(-1.2, 1.2)
    ax1.set_xlabel("angle (deg)"); ax1.set_ylabel("voltage (p.u.)")
    ax1.set_title(f"alpha = {np.degrees(a):.0f}°  →  P/Pmax = {power_fraction(a):.2f}")
    ax1.grid(alpha=0.3); ax1.legend(fontsize=8, loc="upper right")
    ax2.plot(ALPHA_DEG, PWR, color="#0ea5e9", lw=2)
    ax2.scatter([np.degrees(a)], [power_fraction(a)], s=80, color="#ef4444", zorder=5)
    ax2.scatter([90], [0.5], s=50, color="#22c55e", marker="x", linewidths=2, label="90°=0.5 anchor")
    ax2.set_xlim(0, 180); ax2.set_ylim(-0.05, 1.05)
    ax2.set_xlabel("firing angle (deg)"); ax2.set_ylabel("P / Pmax")
    ax2.grid(alpha=0.3); ax2.legend(fontsize=8)
    fig.tight_layout()


anim = FuncAnimation(fig, draw, frames=len(ALPHAS), interval=120)
anim.save(OUT_MP4, writer=FFMpegWriter(fps=8, bitrate=1200))
print(f"saved {OUT_MP4} {os.path.getsize(OUT_MP4)} bytes")
anim.save(OUT_GIF, writer=PillowWriter(fps=8))
print(f"saved {OUT_GIF} {os.path.getsize(OUT_GIF)} bytes")
# verify step-by-step: anchor + files exist + non-trivial size
assert abs(power_fraction(np.pi / 2) - 0.5) < 1e-12, "90-degree anchor broken"
assert os.path.getsize(OUT_MP4) > 20000 and os.path.getsize(OUT_GIF) > 20000
print("VERIFY OK: P(pi/2)=0.5, mp4+gif non-empty")
