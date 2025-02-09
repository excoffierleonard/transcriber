# Transcriber

Transcriber is a simple tool to convert audio files to text. It uses the Whisper Turbo Model.

## Deployment

It is recommended to have an Nvidia GPU with at least 6GB of VRAM to run the model.

```bash
curl -o compose.yaml https://raw.githubusercontent.com/excoffierleonard/transcriber/refs/heads/main/compose.yaml && \
docker compose up -d
```

## Development

### Setup

```bash
git clone https://github.com/excoffierleonard/parser.git && \
cd parser && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt
```

### Run

```bash
python3 src/main.py
```

## TODO

- Add tests
- When a request is canceled, directly stop the transcription