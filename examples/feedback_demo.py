"""Exercise actual feedback logic with scripted posture states, without hardware."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output/feedback-demo"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Import the unchanged app but prohibit physical camera access and suppress audio.
    # MediaPipe initialization still needs a supported desktop graphics environment.
    with patch("cv2.VideoCapture", side_effect=AssertionError("No camera in synthetic demo")), \
         patch("audio_alerts.play_posture_alert"), patch("audio_alerts.play_correction_success"):
        import app
        traces, events, summary = [], [], {}
        times = np.arange(0, 351, dtype=float) / 10
        for condition in ("immediate", "adaptive"):
            sid = "SYNTHETIC_" + condition
            sess = app._new_session("SYNTHETIC_DEMO", condition)
            sess["active"] = True
            app.sessions[sid] = sess
            try:
                for t in times:
                    good = not (2 <= t < 10 or 22 <= t < 30)
                    actions = app._process_posture(sid, {"good": good}, 1000 + float(t))
                    traces.append((condition, float(t), good, sess["alert_active"], sess["delay"]))
                    for action in ("show_alert", "hide_alert", "alert_expired"):
                        if actions.get(action):
                            events.append(dict(condition=condition, seconds=float(t), action=action,
                                               adaptive_delay=sess["delay"]))
                shown = [e["seconds"] for e in events if e["condition"] == condition and e["action"] == "show_alert"]
                hidden = [e["seconds"] for e in events if e["condition"] == condition and e["action"] == "hide_alert"]
                assert shown[0] == (3 if condition == "immediate" else 7)
                assert hidden == [10, 30] and len(shown) == 2
                assert sess["n_ignored"] == 0 and len(sess["latencies"]) == 2
                assert sess["delay"] == (5 if condition == "immediate" else 5.70), (condition, shown, sess["delay"])
                summary[condition] = dict(alert_times=shown, correction_times=hidden,
                                          final_delay=sess["delay"], alerts=sess["n_alerts"])
            finally:
                del app.sessions[sid]
        app.pose.close()
    with (args.output_dir / "feedback-trace.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("condition", "seconds", "scripted_posture_good", "alert_active", "delay_seconds"))
        writer.writerows(traces)
    (args.output_dir / "feedback-events.json").write_text(json.dumps(events, indent=2) + "\n")
    (args.output_dir / "feedback-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.subplots_adjust(left=.16, right=.97, top=.72, bottom=.23)
    fig.text(.045, .94, "Same scripted posture. Different feedback timing.", fontsize=21, weight="bold", color="#0f172a")
    fig.text(.045, .865, "Actual application state machine · 10 Hz synthetic inputs · camera and audio disabled", color="#475569")
    ax.broken_barh([(2, 8), (22, 8)], (2-.16, .32), facecolors="#64748b")
    ax.text(6, 2, "poor posture", color="white", ha="center", va="center", fontsize=10)
    ax.text(26, 2, "poor posture", color="white", ha="center", va="center", fontsize=10)
    for condition, y, color in (("immediate", 1, "#0f766e"), ("adaptive", 0, "#6d28d9")):
        starts = summary[condition]["alert_times"]
        stops = summary[condition]["correction_times"]
        ax.broken_barh([(a, b-a) for a, b in zip(starts, stops)], (y-.16, .32), facecolors=color)
        for start in starts:
            ax.annotate(f"alert {start:g}s", (start, y+.16), xytext=(0, 8), textcoords="offset points",
                        ha="center", fontsize=10, color=color)
        for stop in stops:
            ax.plot(stop, y, marker="|", markersize=22, color="#0f172a")
    ax.set_yticks([0, 1, 2], ["Adaptive", "Immediate", "Scripted input"])
    ax.set_ylim(-.5, 2.6)
    ax.set_xlim(0, 35)
    ax.set_xlabel("Elapsed seconds · alerts clear at scripted corrections (10s and 30s)")
    ax.grid(axis="x", color="#e2e8f0", lw=.7)
    ax.set_axisbelow(True)
    fig.text(.045, .08, "Adaptive delay: 5.00 → 5.30 → 5.70s. Software behavior only; no participant or efficacy results.", fontsize=11, color="#475569")
    fig.savefig(args.output_dir / "feedback-timing.png", dpi=160, facecolor="white")
    plt.close(fig)
    print(json.dumps(summary, indent=2))
    print("PASS: both first-alert thresholds, two corrections per mode, and final adaptive delay.")


if __name__ == "__main__":
    main()
