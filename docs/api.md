# Transcriber APi Documentation

## Endpoints

## Transcribe audio files

### Request

#### Endpoint

```http
POST /transcribe
```

#### Headers

| Key | Value |
|-|-|
| Content-Type | multipart/form-data |

#### Body (multipart/form-data)

| Key | Value |
|-|-|
| file | *One or more audio files to transcribe* |

### Response

#### Status Code

- `200 OK`: The transcription was successful

#### Headers

| Key | Value |
|-|-|
| Content-Type | application/json |

#### Body (application/json)

```json
{
    "texts": [
        "*Transcription of the first audio file*",
        "*Transcription of the second audio file*",
    ]
}
```

### Example

#### Request

```bash
curl --url "http://localhost:8080/transcribe" \
     --request POST \
     --header "Content-Type: multipart/form-data" \
     --form "file=@tests/inputs/test_audio_1.mp3" \
     --form "file=@tests/inputs/test_audio_2.mp3"
```

#### Response

Status Code:
- `200 OK`

Header:

```http
Content-Type: application/json
```

Body:

```json
{
    "texts": [
        "Hello, how are you?",
        "I'm fine, thank you."
    ]
}
```
