# PostureAware

**A collaborative webcam-based study of immediate versus adaptive feedback for sitting posture.**

PostureAware combines MediaPipe pose estimation, individual baseline calibration, a Flask web interface, audio cues, and session summaries. It was developed for Georgia Tech's Health Sensing and Interventions course by **Anna Cho and Amey Agarwal**.

## My contribution — Anna Cho

I led the PostureAware project in collaboration with **Amey Agarwal**. I used AI tools to help generate application code. This portfolio therefore highlights my project leadership and AI-assisted development within a shared course project.

The final report credits both Anna Cho and Amey Agarwal. My role statement reflects my account of the work; the archived Git commits are attributed to Amey and do not capture the full division of work. Individual module ownership and task-by-task percentages are not assigned in this edition.

[Contribution context and team credit](docs/CONTRIBUTIONS.md) · [AI assistance disclosure](AI_USAGE.md) · [Original project](https://github.com/amey-agarwal/CorrectivePosture) · [Data handling](docs/DATA_HANDLING.md)

## What the shared project does

- Registers a local study session and assigns an immediate or adaptive condition.
- Checks lighting and estimates a personal neutral-posture baseline.
- Monitors neck tilt, shoulder tilt, and face proximity using a webcam.
- Uses a 1-second poor-posture threshold for immediate feedback; adaptive feedback starts at 5 seconds and changes with correction latency.
- Produces session summaries and collects a post-session questionnaire.

The joint report describes a 13-person, between-subjects study with 30-minute sessions. That is historical report context, not a result independently reproduced from this data-free edition. The app is a course research prototype, not a clinically validated diagnostic or treatment system.

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

## Checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pip check
```

The tests do not open a camera, play audio, or load participant data. They cover baseline behavior, synthetic lighting, Flask page/registration smoke checks, and temporary-directory record creation. Live tracking accuracy, audio hardware, and real-session behavior require separate manual verification.

## Collaboration, source, and publication status

The upstream recorded in the archive is [amey-agarwal/CorrectivePosture](https://github.com/amey-agarwal/CorrectivePosture). The available history ends at `67a8a88`. This is a curated snapshot, not a preserved-history fork. Both collaborators must remain credited.

**No license file was found in the supplied app snapshot.** No new open-source license is assigned here. Confirm the intended publication/license terms with the collaborator before treating the shared code as licensed for redistribution. See [NOTICE.md](NOTICE.md).

Portfolio preparation added these documents, dependency cleanup, hardware-free checks, and local server defaults: loopback-only binding, debug disabled, a runtime secret key, and default same-origin Socket.IO handling. These are preparation changes made with Codex assistance, not claims about Anna's original coursework implementation. [Source manifest and changes](docs/PROVENANCE.md).
