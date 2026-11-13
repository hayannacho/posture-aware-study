# Validation — 2026-11-13

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
