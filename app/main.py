import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import UPLOAD_DIR
from app.services.gnani_service import GnaniService
from app.services.translation_service import TranslationService
from app.services.form_service import FormExtractionService


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="ArogyaDhwani",
    description="Multilingual healthcare communication assistant",
    version="1.1.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

gnani = GnaniService()
translator = TranslationService()
form_extractor = FormExtractionService(translator)

ALLOWED_AUDIO_TYPES = {".wav", ".mp3", ".m4a", ".ogg", ".webm"}


class SpeechRequest(BaseModel):
    text: str
    language: str = "en-IN"
    voice: str = "Pranav"


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


class FormExtractionRequest(BaseModel):
    transcript: str
    detected_language: str


@app.get("/")
async def home():
    return FileResponse(TEMPLATE_DIR / "index.html")


@app.get("/health")
async def health():
    return {
        "status": "running",
        "application": "ArogyaDhwani",
        "version": "1.1.0",
    }


@app.post("/api/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language_code: str = Form("indic-auto"),
    role: str = Form("patient"),
):
    if role not in {"patient", "doctor"}:
        raise HTTPException(status_code=400, detail="Invalid speaker role.")

    extension = Path(audio.filename or "").suffix.lower()

    if extension not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported audio format.")

    audio_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{extension}"

    try:
        contents = await audio.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Audio file is empty.")

        if len(contents) > 15 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Audio must be smaller than 15 MB.")

        audio_path.write_bytes(contents)

        result = gnani.transcribe_audio(
            audio_path=audio_path,
            language_code=language_code,
            role=role,
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=502,
                detail="Gnani Prisma could not transcribe this audio.",
            )

        return {
            "success": True,
            "transcript": result.get("transcript", ""),
            "detected_language": result.get("detected_language_code", "Not returned"),
            "request_id": result.get("request_id"),
            "role": role,
            "message": "Audio transcribed successfully.",
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Speech transcription failed: {error}")
    finally:
        if audio_path.exists():
            audio_path.unlink()


@app.post("/api/translate")
async def translate_text(request: TranslationRequest):
    try:
        translated = translator.translate_text(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        return {
            "success": True,
            "original_text": request.text,
            "translated_text": translated,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "message": "Translation completed. Please review before use.",
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Translation failed: {error}")


@app.post("/api/extract-form")
async def extract_patient_form(request: FormExtractionRequest):
    try:
        return {
            "success": True,
            **form_extractor.extract(
                request.transcript,
                request.detected_language,
            ),
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Form extraction failed: {error}")


@app.post("/api/speak")
async def generate_doctor_response(request: SpeechRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Please enter text to convert into speech.")

    try:
        audio_bytes = gnani.generate_speech(
            text=request.text,
            language=request.language,
            voice=request.voice,
        )
        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={"Content-Disposition": 'inline; filename="doctor_response.wav"'},
        )
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Speech generation failed: {error}")