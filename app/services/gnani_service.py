from pathlib import Path

from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient

from app.config import GNANI_API_KEY


class GnaniService:
    def __init__(self):
        self.stt_client = GnaniSTTClient(api_key=GNANI_API_KEY)
        self.tts_client = GnaniTTSClient(api_key=GNANI_API_KEY)

    def transcribe_audio(
        self,
        audio_path: str | Path,
        language_code: str = "indic-auto",
        role: str = "patient"
    ) -> dict:

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError("Audio file not found.")

        topic = (
            "Doctor communicating medical guidance to a patient"
            if role == "doctor"
            else "Patient describing symptoms and healthcare concerns"
        )

        return self.stt_client.transcribe(
            audio=audio_path,
            language_code=language_code,
            model="prisma-v3.0",
            format="verbatim",
            topic=topic
        )

    def generate_speech(
        self,
        text: str,
        language: str = "en-IN",
        voice: str = "Pranav"
    ) -> bytes:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        return self.tts_client.synthesize(
            text=text,
            voice=voice,
            model="timbre-v2.5",
            language=language
        )