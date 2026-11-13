# PostureAware

**A webcam application for exploring immediate versus adaptive sitting-posture feedback.**

MediaPipe pose estimation, personal calibration, visual monitoring and optional audio cues come together in a local Flask application. Developed as a team project for Georgia Tech's Health Sensing and Interventions course. AI tools were used to help write application code; see [code-development disclosure](AI_USAGE.md).

## Features and demo outputs

| Step | What the application does |
| --- | --- |
| Calibrate | Check lighting and estimate a personal neutral-posture baseline |
| Monitor | Track neck tilt, shoulder tilt and face proximity |
| Give feedback | Use a 1-second poor-posture threshold for immediate feedback; adaptive feedback starts at 5 seconds and changes with correction latency |
| Summarize | Produce session summaries and a post-session questionnaire |

**Verified:** four hardware-free tests passed, covering baseline calibration, synthetic lighting, Flask registration/pages and temporary synthetic record creation. Live camera tracking, audio and 30-minute sessions have not been revalidated. [Validation details](docs/VALIDATION.md).

**Study context:** the study report describes a 13-person study with 30-minute sessions. No efficacy result is claimed from this data-free edition. This is a course research prototype, not a clinically validated system.

**Participant data excluded:** no original participant records, questionnaires, logs or recordings are published. Running the app can create new local records; see [data handling](docs/DATA_HANDLING.md).

## Run locally

Use **Python 3.11 or 3.12**. Validation details are recorded in [VALIDATION.md](docs/VALIDATION.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` on the same computer. The camera and audio are attached to the Python process on that computer. Run one local user session at a time; the inherited global camera/pose/session design is not a multi-user service.

**Audio is optional for installation, but required to evaluate the study's audible feedback.** Without PyAudio, the app runs silently with an explicit warning. See [SETUP.md](SETUP.md) for audio installation. Do not interpret a silent demo as a reproduction of the original intervention.

The core application performs pose processing locally and writes records under `data/`. The monitor page loads Socket.IO JavaScript from a CDN, so this edition is not entirely offline. It is not configured to upload study records to an analytics service.

## Checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pip check
```

The tests do not open a camera, play audio, or load participant data. They cover baseline behavior, synthetic lighting, Flask page/registration smoke checks, and temporary-directory record creation. Live tracking accuracy, audio hardware, and real-session behavior require separate manual verification.

## Development and source

The application integrates personal-baseline calibration, posture monitoring, feedback timing and local study-session records. AI tools were used to help generate application code. [Code-development disclosure](AI_USAGE.md) · [Source and changes](docs/PROVENANCE.md).

## Participant data excluded

No original questionnaire responses, participant IDs/rows, alert logs, session summaries, or recordings are included. Tests create clearly labeled synthetic records only in temporary directories. Running the application yourself can create new local records; `.gitignore` excludes these, but is not an anonymization mechanism.

Do not add original participant folders, `data/`, exports, screenshots of individual records, or original Git history to a public copy. See [the data-handling notes](docs/DATA_HANDLING.md).

## Files

```text
app.py                 Local Flask/Socket.IO app and study logic
calibration.py         Lighting and personal-baseline calibration
audio_alerts.py        Optional generated chimes
templates/             Registration, calibration, monitor, survey, results
requirements*.txt      Core, optional audio, and test dependencies
tests/                 New hardware-free preparation checks
docs/                  Contribution, provenance, data handling, validation
```

Original setup scripts that repeatedly installed conflicting OpenCV packages are omitted. The old setup guide referenced `analyze_results.py` and `export_data.py`, which are absent from the supplied app snapshot; this edition does not advertise those commands or claim to reproduce the original study statistics.

## Source and licensing

The upstream recorded in the archive is [amey-agarwal/CorrectivePosture](https://github.com/amey-agarwal/CorrectivePosture). The available history ends at `67a8a88`. This is a curated snapshot, not a preserved-history fork. Source provenance is retained in the documentation.

**No license file was found in the supplied app snapshot.** No new open-source license is assigned here. The repository does not grant additional redistribution rights. See [NOTICE.md](NOTICE.md).

Portfolio preparation added these documents, dependency cleanup, hardware-free checks, and local server defaults: loopback-only binding, debug disabled, a runtime secret key, and default same-origin Socket.IO handling. These are publication-preparation changes, not claims about the original coursework implementation. [Source manifest and changes](docs/PROVENANCE.md).
