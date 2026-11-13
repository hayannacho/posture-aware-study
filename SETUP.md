# Local setup

Use Python 3.11 or 3.12. The version bounds retain the original MediaPipe `mp.solutions.pose` API and NumPy 1.x compatibility. Do not separately install `opencv-python` alongside `opencv-contrib-python`.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. No participant dataset is needed. Use a clearly synthetic ID for an exploratory demo, and do not enter real demographics unless intentionally conducting an authorized study.

## Optional audio

On macOS install the PortAudio library with your package manager (`brew install portaudio`), then:

```bash
python -m pip install -r requirements-audio.txt
```

On Debian/Ubuntu the development package is `portaudio19-dev`; Windows may use a compatible PyAudio wheel. Audio hardware has not been verified in this preparation. If PyAudio is unavailable, the existing module warns and falls back to silence.

## Local operation

- The app opens the webcam when a video stream is requested. Grant camera access to the Python/terminal application if the OS asks.
- Camera frames are handled by the local Python process; do not use a remote host for a personal webcam demo.
- The server binds to `127.0.0.1`, with debug disabled. It is not intended as a public hosted service.
- The monitor page retrieves Socket.IO JavaScript from cdnjs. Internet access is therefore needed for that asset unless it is separately vendored with its license.
- A runtime secret is generated automatically; optionally supply `POSTURE_SECRET_KEY` via the environment. Never commit environment files or actual secret values.
- If port 5000 is occupied, stop the conflicting app or adjust the local port in the entry point and use the matching URL.

## Data and exports

New session and questionnaire files are saved to `data/`, which is ignored by Git. The application includes an `/api/export/<session_id>` endpoint that returns a summary and file paths; it is not a ZIP-download script. No `export_data.py` or `analyze_results.py` is supplied in this edition.

The app's original saving logic uses participant ID and condition in filenames. Reusing the same ID/condition can overwrite an earlier summary. Treat this as a local prototype limitation when designing any future study.
