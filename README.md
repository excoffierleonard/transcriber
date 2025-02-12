# [Transcriber](https://transcriber.excoffierleonard.com)

Transcriber is a simple tool to convert audio files to text. It uses the Whisper Turbo Model.

Demonstration URL: [https://transcriber.excoffierleonard.com](https://transcriber.excoffierleonard.com)

Demonstration Endpoint: [https://transcriber.excoffierleonard.com/transcribe](https://transcriber.excoffierleonard.com/transcribe)

```bash
curl https://transcriber.excoffierleonard.com/transcribe \
     -F "file=@tests/inputs/test_audio_1.mp3"
```

## 📚 Table of Contents

- [⚙ Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
- [🧪 Development](#-development)
- [📖 API Documentation](#-api-documentation)
- [📜 License](#-license)

## ⚙ Configuration

The configuration is done through environment variables.

- `TRANSCRIBER_APP_PORT`: The port on which the application will listen. (Default is `8080`)
- `MODEL_IDLE_TIMEOUT`: The time in seconds after which the model will be unloaded if it is not used. (Default is `300`, set to `0` to never unload the model)
- `ENABLE_FRONTEND`: Enable the frontend. (Default is `false`)

## 🚀 Deployment

It is recommended to have an Nvidia GPU with at least 6GB of VRAM to run the model.

```bash
curl -o compose.yaml https://raw.githubusercontent.com/excoffierleonard/transcriber/refs/heads/main/compose.yaml && \
docker compose up -d
```

## 🧪 Development

### Setup

```bash
git clone https://github.com/excoffierleonard/transcriber.git && \
cd transcriber && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt
```

### Run

```bash
python3 src/main.py
```

### Tests

```bash
pytest
```

## 📖 API Documentation

API documentation and examples are available in [docs/api.md](docs/api.md).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## TODO

- When a long request is canceled, directly stop the transcription, dont wait for the transcription to finish

