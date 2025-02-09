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

# Run the application
CMD ["python", "src/main.py"]
