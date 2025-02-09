from flask import Flask, request, jsonify
import whisper
import tempfile
import threading
import os

app = Flask(__name__)

# Get idle timeout from env (default to 300 seconds = 5 minutes)
MODEL_IDLE_TIMEOUT = int(os.environ.get("MODEL_IDLE_TIMEOUT", 300))
TRANSCRIBER_APP_PORT = int(os.environ.get("TRANSCRIBER_APP_PORT", 8080))

# Global variables for the model and idle timer
model = None
model_lock = threading.Lock()  # Protects access to the model
idle_timer = None
timer_lock = threading.Lock()  # Protects access to the idle timer


def load_model():
    """Load the Whisper model."""
    global model
    model = whisper.load_model("turbo")
    print("Model loaded.")


def unload_model():
    """
    Unload the model if no activity has occurred for the idle timeout.
    This deletes the model reference, empties the GPU cache (if applicable),
    and triggers garbage collection.
    """
    global model, idle_timer
    with model_lock:
        if model is not None:
            print("Unloading model due to inactivity...")
            # Remove the model reference.
            temp_model = model
            model = None
            del temp_model

            # Attempt to free GPU memory and perform garbage collection.
            try:
                import torch

                torch.cuda.empty_cache()
            except ImportError:
                pass  # torch might not be installed or used.
            import gc

            gc.collect()
            print("Model successfully unloaded.")
    with timer_lock:
        idle_timer = None


def reset_idle_timer():
    """
    Cancel any existing idle timer and start a new one.
    When the timer expires, unload_model will be called.
    """
    global idle_timer
    with timer_lock:
        if idle_timer is not None:
            idle_timer.cancel()
        idle_timer = threading.Timer(MODEL_IDLE_TIMEOUT, unload_model)
        idle_timer.daemon = True  # so that the timer thread doesn't block app exit
        idle_timer.start()


def ensure_model_loaded():
    """
    Ensure that the model is loaded.
    If not, load it and then (re)start the idle timer.
    """
    global model
    with model_lock:
        if model is None:
            print("Loading model...")
            load_model()
    reset_idle_timer()


def save_temp_file(file):
    """Save the uploaded file to a temporary file and return its path."""
    temp_audio = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_audio.name)
    return temp_audio.name


def post_process(text):
    """
    Strip leading/trailing whitespace, capitalize the first character,
    and add a period at the end if missing.
    """
    text = text.strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    # TODO: Maybe find more elegant way to check for sentence end
    if text and not text.endswith((".", "?", "!", ";", ":")):
        text += "."
    return text


def transcribe_file(file_path):
    """Transcribe the audio file using the Whisper model and post-process the result."""
    # Ensure the model is loaded (and reset the idle timer)
    ensure_model_loaded()
    with model_lock:
        result = model.transcribe(file_path)
    transcription = post_process(result["text"])
    return transcription


@app.route("/transcribe", methods=["POST"])
def transcribe():
    files = request.files.getlist("file")
    transcriptions = []
    for file in files:
        temp_file_path = save_temp_file(file)
        transcription = transcribe_file(temp_file_path)
        transcriptions.append(transcription)
    return jsonify({"texts": transcriptions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=TRANSCRIBER_APP_PORT)
