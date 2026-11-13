# Source and preparation changes

Source prefix: `GATECH/Summer2026/HSI/PostureStudy/` inside the supplied `GATECH.zip`.

[Source manifest](source-manifest.json) lists the eight selected original application files and their SHA-256 hashes before preparation edits. The original repository history was inspected separately for attribution, not copied to this folder.

## Intentional app.py changes

- Replace the hard-coded Flask secret with `POSTURE_SECRET_KEY` or an automatically generated runtime secret.
- Remove the wildcard Socket.IO origin setting, retaining the default same-origin handling.
- Bind the development server to `127.0.0.1` with debug disabled.

Calibration, audio logic, templates, feedback timing, analysis, and record formats are otherwise preserved. The loopback/default-origin setup must be manually checked with a real browser and camera before running a study.

## New preparation files

README, SETUP, attribution/license-status notice, dependency files, .gitignore, source manifest, tests and validation notes. New tests use synthetic inputs and temporary output only.

## Omitted

Participant records, full report/poster, original Git history, virtual environments, copied desktop metadata, missing analysis/export scripts, and old setup scripts that installed duplicate OpenCV distributions. The curated edition is intended for hayannacho/posture-aware-study.
