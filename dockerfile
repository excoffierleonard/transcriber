FROM python:3.11-slim

# Install system dependencies
RUN apt update && apt install -y \
    ffmpeg

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Preload Whisper's Turbo model
RUN python -c "import whisper; whisper.load_model('turbo')"

# Copy source code
COPY src src/

# Run the application (with one worker since whisper does not support parallelism)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "src.main:app", "--access-logfile", "-", "--workers", "1"]
