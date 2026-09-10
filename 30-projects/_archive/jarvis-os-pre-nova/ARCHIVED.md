# Archived — superseded by `30-projects/nova`

This is the earlier **JARVIS** iteration of the voice-assistant project, kept
for reference. The live version is `30-projects/nova`.

What changed in N.O.V.A:
- Renamed JARVIS → N.O.V.A throughout (persona, UI, wordmark).
- Speaking moved from ElevenLabs to **Kokoro**, running locally — no API key,
  no quota, no network call. See `requirements-kokoro.txt`.
- ElevenLabs now handles **listening** (speech-to-text) only, with the
  browser's own speech recognition as a fallback when no key is present.
- Speaking and listening now fail independently rather than together.

Full history for both versions is in git; this folder can be deleted at any
time without losing it.
