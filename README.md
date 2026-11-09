# ArogyaDhwani
### Multilingual Voice Communication Support for Healthcare

**Breaking language barriers. Making healthcare conversations clearer.**

ArogyaDhwani is an AI-powered, voice-first healthcare communication prototype designed to help patients and healthcare professionals communicate across language differences.

It combines speech recognition, language translation, smart patient-detail extraction, and text-to-speech using Gnani.ai voice technology.

---

## The Problem

Language differences can make healthcare conversations difficult. Patients may struggle to explain their symptoms, while healthcare professionals may not understand important details accurately.

Manual translation and repeated typing can interrupt the consultation process.

## Our Solution

ArogyaDhwani creates a multilingual communication flow that allows patients and healthcare professionals to speak in supported languages, view recognised text, translate messages, and organise explicitly stated patient information.

## Key Features

- **Multilingual Speech Recognition:** Converts spoken input into text using Gnani.ai Prisma STT.
- **Six Supported Languages:** English, Hindi, Kannada, Tamil, Telugu, and Malayalam.
- **Language Translation:** Translates recognised text into the selected language.
- **Smart Form Filling:** Extracts explicitly mentioned patient details from multi-sentence transcripts and maps them to relevant form fields.
- **Text-to-Speech:** Converts text into spoken audio using Gnani.ai Timbre TTS.
- **Visible Transcripts:** Displays recognised and translated text for review.
- **Human-in-the-Loop:** Keeps healthcare professionals involved in reviewing communication and extracted information.

## How It Works

1. The patient speaks in a supported language.
2. Gnani.ai Prisma converts speech into text.
3. The recognised text is translated into the selected language.
4. Smart Form Filling extracts explicitly stated patient details.
5. The healthcare professional can review the information.
6. Text can be converted into speech using Gnani.ai Timbre.

## Technology Stack

| Component | Technology |
|---|---|
| Speech-to-Text | Gnani.ai Prisma |
| Text-to-Speech | Gnani.ai Timbre |
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Translation | MyMemory Translation API |

## Project Structure

```text
ArogyaDhwani/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   └── services/
│       ├── gnani_service.py
│       ├── translation_service.py
│       ├── form_service.py
│       └── extraction_service.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   └── index.html
│
├── tests/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Monika-2108/ArogyaDhwani.git
cd ArogyaDhwani
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate it on Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Configure your API