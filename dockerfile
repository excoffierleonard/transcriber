FROM debian:stable-slim

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/app"

# Install system dependencies
RUN apt update && apt install -y \
    curl \
    ffmpeg

# Set working directory
WORKDIR /app

# uv Installation
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Python dependencies
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync

# Pre-download Whisper's Turbo model
COPY scripts scripts/
RUN uv run scripts/download_model.py

# Copy source code
COPY src src/

# Set runtime environment variables
ENV MODEL_IDLE_TIMEOUT=300
ENV ENABLE_FRONTEND=false

# Run the application (with one worker since whisper does not support parallelism)
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:8080", "src.main:app", "--access-logfile", "-", "--workers", "1", "--timeout", "3600"]
