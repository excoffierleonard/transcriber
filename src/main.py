from flask import Flask, request, jsonify
import whisper
import tempfile

# Initialize Flask app
app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("turbo")

def save_temp_file(file):
    """Save the uploaded file to a temporary file and return the file path."""
    temp_audio = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_audio.name)
    return temp_audio.name

def transcribe_file(file_path):
    """Transcribe the audio file using the Whisper model."""
    result = model.transcribe(file_path)
    return result["text"]

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
