"""
Voice: Kokoro (local, offline) for speech out, ElevenLabs for speech in.

Kokoro runs entirely on this machine — no key, no quota, no network call for
speaking. It needs `pip install kokoro soundfile` (torch comes in as its
dependency) and, on first run, downloads the ~300MB Kokoro-82M model from
Hugging Face. See requirements-kokoro.txt.

ElevenLabs still handles listening (speech-to-text) — Kokoro doesn't do STT.
Set ELEVENLABS_API_KEY for that; without it, transcribe() raises and the
browser's own speech recognition takes over (see ui/app.js).
"""
import io
import json
import os
import threading
import urllib.error
import urllib.request

# ── speaking: Kokoro, local ─────────────────────────────────────────
KOKORO_VOICE = os.environ.get("KOKORO_VOICE", "bm_george")   # British Male · George
KOKORO_LANG = os.environ.get("KOKORO_LANG", "b")             # 'b' = British English
SAMPLE_RATE = 24000

_KOKORO_LOCK = threading.Lock()
_KOKORO_PIPELINE = None


def tts_available():
    try:
        import kokoro          # noqa: F401
        return True
    except ImportError:
        return False


def _get_pipeline():
    global _KOKORO_PIPELINE
    if _KOKORO_PIPELINE is None:
        from kokoro import KPipeline
        _KOKORO_PIPELINE = KPipeline(lang_code=KOKORO_LANG)
    return _KOKORO_PIPELINE


def speak(text):
    """Returns WAV bytes from local Kokoro TTS, or raises."""
    text = (text or "").strip()
    if not text:
        raise ValueError("empty text")
    if not tts_available():
        raise RuntimeError("kokoro not installed — pip install kokoro soundfile")

    import numpy as np
    import soundfile as sf

    # No length cap — Kokoro is local and free, unlike the ElevenLabs setup
    # this was originally written for. Kokoro itself chunks internally.

    # Model load + inference aren't safe to run concurrently across requests.
    with _KOKORO_LOCK:
        pipeline = _get_pipeline()
        chunks = [r.audio.numpy() for r in pipeline(text, voice=KOKORO_VOICE)]

    if not chunks:
        raise RuntimeError("kokoro produced no audio")
    audio = np.concatenate(chunks)
    buf = io.BytesIO()
    sf.write(buf, audio, SAMPLE_RATE, format="WAV")
    return buf.getvalue()


# ── listening: ElevenLabs Scribe ────────────────────────────────────
def stt_available():
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def transcribe(audio, mime="audio/webm"):
    """Speech to text via ElevenLabs Scribe. Returns the transcript, or raises.

    No local speech-to-text here — Kokoro is TTS-only. When this isn't
    available (no key, quota, network), the browser's own SpeechRecognition
    takes over instead (see ui/app.js browserListen()).
    """
    if not stt_available():
        raise RuntimeError("no ELEVENLABS_API_KEY")
    if not audio:
        raise ValueError("empty audio")

    ext = {"audio/webm": "webm", "audio/ogg": "ogg", "audio/mp4": "mp4",
           "audio/mpeg": "mp3", "audio/wav": "wav"}.get(mime.split(";")[0], "webm")
    boundary = "----jarvis" + os.urandom(8).hex()
    b = boundary.encode()

    body = b"".join([
        b"--", b, b"\r\n",
        b'Content-Disposition: form-data; name="model_id"\r\n\r\nscribe_v1\r\n',
        b"--", b, b"\r\n",
        f'Content-Disposition: form-data; name="file"; filename="turn.{ext}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        audio, b"\r\n",
        b"--", b, b"--\r\n",
    ])

    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/speech-to-text",
        data=body, method="POST",
        headers={
            "content-type": f"multipart/form-data; boundary={boundary}",
            "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
        },
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return (json.loads(r.read()).get("text") or "").strip()


def voices():
    """List the account's ElevenLabs voices (STT key only — unrelated to Kokoro)."""
    if not stt_available():
        return []
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v2/voices",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = json.loads(r.read())
    except (urllib.error.URLError, urllib.error.HTTPError):
        return []
    return [dict(id=v.get("voice_id"), name=v.get("name"),
                 labels=v.get("labels", {}))
            for v in body.get("voices", [])]
