from flask import Flask, request, jsonify
import whisper
import tempfile
from threading import Lock

# Initialize Flask app
app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("turbo")

# Create a lock to prevent concurrent access to the model
model_lock = Lock()

def save_temp_file(file):
    """Save the uploaded file to a temporary file and return the file path."""
    temp_audio = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_audio.name)
    return temp_audio.name

def post_process(text):
    """
    Strip leading/trailing whitespace, capitalize the first character, and add a period at the end if missing.
    Note: .capitalize() would lowercase the rest of the string, so here we
    only modify the first character if needed.
    """
    text = text.strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    if text and not text.endswith('.'):
        text += '.'
    return text


def transcribe_file(file_path):
    """Transcribe the audio file using the Whisper model and post-process the result."""
    with model_lock:
        result = model.transcribe(file_path)
    transcription = result["text"]
    transcription = post_process(transcription)
    return transcription

@app.route('/transcribe', methods=['POST'])
def transcribe():
    files = request.files.getlist('file')
    transcriptions = []

    for file in files:
        temp_file_path = save_temp_file(file)
        transcription = transcribe_file(temp_file_path)
        transcriptions.append(transcription)

    return jsonify({"texts": transcriptions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
