from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)
model = whisper.load_model("turbo")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    files = request.files.getlist('file')
    transcriptions = []

    for file in files:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile() as temp_audio:
            file.save(temp_audio.name)
            result = model.transcribe(temp_audio.name)
            transcriptions.append(result["text"])

    return jsonify({"texts": transcriptions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
