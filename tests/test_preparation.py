"""Preparation checks: synthetic inputs only; no camera/audio or study records."""
from pathlib import Path
import numpy as np
import pytest
import calibration


def test_baseline_requires_minimum_samples(monkeypatch):
    monkeypatch.setattr(calibration.audio_alerts, 'play_calibration_complete', lambda: None)
    cal = calibration.CalibrationSession()
    for _ in range(19):
        cal.add_posture_sample({'neck_tilt': 10., 'shoulder_tilt': 2., 'face_proximity': .5})
    assert cal.finalize_baseline() is None
    cal.add_posture_sample({'neck_tilt': 1000., 'shoulder_tilt': 1000., 'face_proximity': 1000.})
    baseline = cal.finalize_baseline()
    assert baseline['neck_tilt'] == 10.
    assert baseline['shoulder_tilt'] == 2.
    assert baseline['face_proximity'] == .5
    assert baseline['n_samples'] == 20
    assert cal.stage == 'audio'


def test_synthetic_lighting_rejects_dark_frames():
    cal = calibration.CalibrationSession()
    for _ in range(20):
        cal.add_lighting_frame(np.zeros((8, 8, 3), dtype=np.uint8))
    assert cal.lighting_status()['ok'] is False


@pytest.fixture
def application(monkeypatch, tmp_path):
    import cv2
    def prohibit_camera(*args, **kwargs):
        raise AssertionError('Tests must never open a camera')
    monkeypatch.setattr(cv2, 'VideoCapture', prohibit_camera)
    import app as module
    module.app.config['TESTING'] = True
    monkeypatch.setattr(module, 'DATA_DIR', str(tmp_path))
    monkeypatch.setattr(module, 'QUESTIONNAIRE_MASTER_CSV', str(tmp_path / 'questionnaire_responses.csv'))
    module.sessions.clear()
    module.calibrations.clear()
    yield module
    module.sessions.clear()
    module.calibrations.clear()


def test_registration_and_pages_without_hardware(application):
    client = application.app.test_client()
    assert client.get('/').status_code == 200
    response = client.post('/api/register', json={'participant_id': 'SYNTHETIC_DEMO', 'condition': 'adaptive'})
    assert response.status_code == 200
    sid = response.json['session_id']
    assert client.get(response.json['redirect']).status_code == 200
    assert client.get(f'/monitor/{sid}').status_code == 200
    assert client.get(f'/questionnaire/{sid}').status_code == 200
    assert application.sessions[sid]['active'] is False


def test_generated_records_are_confined_to_test_tempdir(application, tmp_path):
    sid = 'synthetic_session'
    application.sessions[sid] = application._new_session('SYNTHETIC_DEMO', 'immediate')
    summary, alert_path, summary_path = application._save_session(sid)
    assert summary['participant_id'] == 'SYNTHETIC_DEMO'
    assert Path(alert_path).parent == tmp_path
    assert Path(summary_path).parent == tmp_path
    assert set(p.name for p in tmp_path.iterdir()) == {'SYNTHETIC_DEMO_immediate_alerts.csv', 'SYNTHETIC_DEMO_immediate_summary.json'}
