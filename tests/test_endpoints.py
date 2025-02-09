import os
import sys
import os
import pytest

# Add the parent directory (project root) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_transcribe_endpoint_success(client):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path1 = os.path.join(current_dir, "inputs", "test_audio_1.mp3")
    input_file_path2 = os.path.join(current_dir, "inputs", "test_audio_2.mp3")

    with open(input_file_path1, "rb") as audio_file1, open(
        input_file_path2, "rb"
    ) as audio_file2:
        data = {
            "file": [
                (audio_file1, "test_audio_1.mp3"),
                (audio_file2, "test_audio_2.mp3"),
            ]
        }
        response = client.post(
            "/transcribe",
            data=data,
            content_type="multipart/form-data",
        )

    expected_response = {"texts": ["Hello, how are you?", "I'm fine, thank you."]}

    assert response.status_code == 200
    assert response.get_json() == expected_response
