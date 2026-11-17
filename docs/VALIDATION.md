# Validation — 2026-11-13

## Synthetic feedback visualization — 2026-11-17

The existing suite passed **4 tests**, retaining three dependency warnings, on Python 3.12.14. `examples/feedback_demo.py` additionally exercises the unchanged `_process_posture` function with the same 351 generated classifications per condition (10 Hz, 0–35 seconds). It blocks `cv2.VideoCapture` and replaces audio calls with mocks. No camera, participant records, or session-file save functions are used. MediaPipe initialization still occurs; pose classification itself is not evaluated.

Two poor-posture intervals start at 2s and 22s; scripted corrections occur at 10s and 30s. Immediate alerts occur at 3s and 23s; adaptive alerts at 7s and 27.4s. Both modes clear on both corrections and report two alerts with no ignored alerts. Adaptive delay changes 5.00 → 5.30 → 5.70 seconds. Assertions check the first thresholds, both corrections, alert counts, and final delay.

Inputs are evaluated with timestamps 1000 + elapsed seconds. At the second adaptive threshold, binary floating-point subtraction leaves the 27.3s sample just below 5.3 seconds; the next 0.1s sample triggers the alert. This observed behavior is preserved, not smoothed in the figure. Corrections are scripted inputs, not human response measurements.

Matplotlib 3.11.2 renders the inspected PNG. [Trace](demo/feedback-trace.csv), [events](demo/feedback-events.json), and [summary](demo/feedback-summary.json) contain only generated behavior. The plot does not establish pose accuracy, audible feedback, efficacy, or real-browser streaming behavior.

Environment: macOS 26.2 arm64, Python 3.12, a new temporary virtual environment.

| Check | Observed result |
| --- | --- |
| Install `requirements-dev.txt` | Succeeded |
| `python -m pytest -q` | **4 passed**, 3 dependency deprecation warnings, 0.97 seconds |
| MediaPipe pose initialization | Succeeded with normal desktop graphics access |
| Camera use | Blocked by the test fixture; no webcam was opened |
| Original source comparison | Only `app.py` changed, as documented in PROVENANCE.md; other selected source files match their original hashes |
| Participant files | Allowlist extraction excludes all original participant datasets and original Git history |

The tests cover median-based baseline calibration with an outlier, minimum sample rejection, synthetic dark-frame detection, registration and page rendering, and writing synthetic session records exclusively into a test temporary directory. They do not verify actual camera tracking, audio output, a 30-minute session, study statistics, or real-browser Socket.IO behavior.

## Environment caveats

A sandboxed attempt could not create the macOS OpenGL context required during MediaPipe initialization. The same tests passed outside that sandbox without camera access.

`pip check` reports that MediaPipe 0.10.21 is not supported on this platform. The downloaded wheel is named universal2, but its installed WHEEL metadata declares `macosx_14_0_x86_64` while the host is arm64. Actual import and pose initialization passed. This metadata discrepancy is recorded rather than hidden; a universally clean dependency check is not claimed. Other platforms and Python 3.11 have not been tested here.

The retained Eventlet backend emits a deprecation warning. This preparation does not migrate the inherited application's asynchronous architecture. The two other warnings concern protobuf type behavior in future Python 3.14; the documented runtime is Python 3.11/3.12.

Exact installed versions are recorded in `constraints-tested.txt`. These constraints describe the tested environment and do not resolve the upstream MediaPipe wheel metadata warning.
