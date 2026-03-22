---
name: ai-multimodal
description: Analyze images/audio/video/docs with Gemini (native, no setup). Generate images (Imagen 4) and videos (Veo 3) via external Gemini API. Use for vision analysis, transcription, OCR, design extraction, image/video generation.
license: MIT
argument-hint: "[file-path] [prompt]"
---

# AI Multimodal

Two modes depending on the task:

| Mode                | Use Case                                     | Setup Required                      |
| ------------------- | -------------------------------------------- | ----------------------------------- |
| **Native Analysis** | Vision, OCR, audio, video analysis, PDF/docs | None — uses built-in Gemini         |
| **Generation**      | Image gen (Imagen 4), video gen (Veo 3)      | `GEMINI_API_KEY` + external scripts |

---

## Mode 1: Native Analysis (No Setup)

Copilot uses Gemini natively. Attach files to the conversation and describe your task.

### Supported Inputs

- **Images**: PNG, JPEG, WEBP — analysis, OCR, design extraction
- **Audio**: WAV, MP3, AAC (up to 9.5h) — transcription, non-speech analysis
- **Video**: MP4, MOV (up to 6h) — scene analysis, temporal Q&A, transcription
- **Documents**: PDF (up to 1000 pages), screenshots — text extraction, summarization

### Usage Patterns

**Image analysis / OCR:**

```
Attach image → "Extract all text from this image" or "Describe this UI layout"
```

**Audio transcription:**

```
Attach audio file → "Transcribe this, include timestamps every 30 seconds"
```

> If audio > 15 min: split into 15-min chunks (ffmpeg) and transcribe each segment separately for a complete result.

**Video analysis:**

```
Attach video → "Identify scene changes and summarize each section"
```

> If video > 15 min: extract audio with ffmpeg, transcribe in 15-min segments, combine results.

**Transcription Output Requirements:**

- Format: Markdown
- Metadata: Duration, file size, date, description, topics covered
- Timestamp format: `[HH:MM:SS -> HH:MM:SS] transcript content`

### For UI / Screenshot Analysis

Use the `multimodal` agent — specialized for UI screenshots, design mockups, wireframes, and visual debugging.

---

## Mode 2: Generation (Requires External Setup)

> ⚠️ **Requires:** `GEMINI_API_KEY` environment variable + `gemini` CLI or external scripts.
> Note: Python scripts are not included in this plugin and have not been reviewed for this runtime.

### Setup

```bash
export GEMINI_API_KEY="your-key"  # https://aistudio.google.com/apikey
```

### Image Generation

If `gemini` CLI is available:

```bash
echo "A photorealistic mountain at sunset" | gemini -y -m imagen-4.0-generate-001
```

Models: `imagen-4.0-generate-001` (standard) · `imagen-4.0-ultra-generate-001` (quality) · `imagen-4.0-fast-generate-001` (speed)

### Video Generation

Veo 3 (`veo-3.1-generate-preview`) — 8s clips with audio. Requires external script setup. See `references/video-generation.md`.

### API Key Rotation (Optional)

```bash
export GEMINI_API_KEY="key1"
export GEMINI_API_KEY_2="key2"  # used on rate limit (429)
export GEMINI_API_KEY_3="key3"
```

---

## References

| Topic          | File                                 | Description                                                                     |
| -------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| Vision         | `references/vision-understanding.md` | Captioning, classification, VQA, detection, OCR, multi-image, structured output |
| Image Gen      | `references/image-generation.md`     | Imagen 4 models, aspect ratios, editing, style/quality control, safety settings |
| Audio          | `references/audio-processing.md`     | Transcription, timestamps, speaker detection, TTS, File API, best practices     |
| Music          | `references/music-generation.md`     | Lyria RealTime API, style prompts, real-time control                            |
| Video Analysis | `references/video-analysis.md`       | Formats, clipping, FPS, temporal Q&A, transcription, optimization               |
| Video Gen      | `references/video-generation.md`     | Veo models, text-to-video, image-to-video, camera control, configuration        |

## Limits

**Sizes**: 20MB inline, 2GB File API
**Formats**: Audio (WAV/MP3/AAC, 9.5h), Images (PNG/JPEG/WEBP), Video (MP4/MOV, 6h), PDF (1k pages)
