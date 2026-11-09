import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


LANGUAGES = {
    "en-IN": "en",
    "hi-IN": "hi",
    "kn-IN": "kn",
    "ta-IN": "ta",
    "te-IN": "te",
    "ml-IN": "ml",
    "en": "en",
    "hi": "hi",
    "kn": "kn",
    "ta": "ta",
    "te": "te",
    "ml": "ml",
}


class TranslationService:
    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        source = LANGUAGES.get(source_language)
        target = LANGUAGES.get(target_language)

        if not source or not target:
            raise ValueError(
                "Unsupported language. Select a supported language first."
            )

        if source == target:
            return text.strip()

        if len(text.encode("utf-8")) > 500:
            raise ValueError(
                "Text is too long for one translation request. "
                "Please use a shorter sentence."
            )

        params = urlencode({
            "q": text,
            "langpair": f"{source}|{target}"
        })

        url = f"https://api.mymemory.translated.net/get?{params}"

        request = Request(
            url,
            headers={"User-Agent": "ArogyaDhwani/1.0"}
        )

        try:
            with urlopen(request, timeout=20) as response:
                result = json.loads(response.read().decode("utf-8"))

            if result.get("responseStatus") != 200:
                raise RuntimeError(
                    result.get("responseDetails", "Translation failed.")
                )

            translated = (
                result.get("responseData", {}).get("translatedText", "")
            )

            if not translated:
                raise RuntimeError("No translated text was returned.")

            return translated

        except HTTPError as error:
            if error.code == 429:
                raise RuntimeError(
                    "Translation daily limit reached. Please try later."
                )
            raise RuntimeError(
                f"Translation service returned HTTP {error.code}."
            )

        except URLError:
            raise RuntimeError(
                "Could not connect to the translation service. "
                "Check your internet connection."
            )