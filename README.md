# Transcriber

Transcriber is a simple tool to convert audio files to text. It uses the Whisper Turbo Model.

## Configuration

The configuration is done through environment variables.

- `TRANSCRIBER_APP_PORT`: The port on which the application will listen. (Default is `8080`)
- `MODEL_IDLE_TIMEOUT`: The time in seconds after which the model will be unloaded if it is not used. (Default is `300`)

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