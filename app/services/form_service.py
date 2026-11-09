import re


class FormExtractionService:
    SUPPORTED_LANGUAGES = {
        "en-IN", "hi-IN", "kn-IN",
        "ta-IN", "te-IN", "ml-IN"
    }

    NUMBER_WORDS = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20, "thirty": 30,
        "forty": 40, "fifty": 50, "sixty": 60,
        "seventy": 70, "eighty": 80, "ninety": 90,
    }

    def __init__(self, translator):
        self.translator = translator

    def _translate(self, text, source):
        if source == "en-IN":
            return text

        chunks = []
        current = ""

        for word in re.findall(r"\S+\s*", text):
            if current and len((current + word).encode("utf-8")) > 400:
                chunks.append(current.strip())
                current = ""
            current += word

        if current.strip():
            chunks.append(current.strip())

        return " ".join(
            self.translator.translate_text(
                text=chunk,
                source_language=source,
                target_language="en-IN",
            )
            for chunk in chunks
        )

    def _number(self, value):
        value = value.lower().strip()

        if value.isdigit():
            number = int(value)
            return str(number) if 0 <= number <= 120 else ""

        parts = re.split(r"[- ]+", value)
        if not parts or len(parts) > 2:
            return ""

        if not all(part in self.NUMBER_WORDS for part in parts):
            return ""

        number = sum(self.NUMBER_WORDS[p] for p in parts)
        return str(number) if number <= 120 else ""

    def extract(self, original_text, detected_language):
        original_text = (original_text or "").strip()
        language = (detected_language or "").strip()

        if not original_text:
            raise ValueError("Patient transcript is empty.")

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError("Unsupported or undetected patient language.")

        english = self._translate(original_text, language)
        text = re.sub(r"\s+", " ", english).strip()

        result = {
            "name": "",
            "age": "",
            "duration": "",
            "allergies": "",
            "medications": "",
            "symptoms": original_text,
            "translated_text": text,
            "detected_language": language,
        }

        name = re.search(
            r"\b(?:my\s+)?name(?:\s+is)?\s+([a-z][a-z '-]{0,49})",
            text, re.I
        )
        if name:
            result["name"] = re.split(
                r"\b(?:and\s+)?(?:i am|i'm|i have|age is)\b",
                name.group(1), flags=re.I
            )[0].strip(" .,-")

        age = re.search(
            r"\b(?:i am|i'm|age is|aged)\s+(?:age\s+is\s+)?"
            r"(\d{1,3}|[a-z]+(?:[- ][a-z]+)?)(?=\s*(?:years?\b|[.,!?;]|$))"
            r"(?:\s+years?\s*old|\s+years?)?\b",
            text, re.I
        )
        if age:
            result["age"] = self._number(age.group(1))

        negative_fever = bool(re.search(
            r"\b(?:no fever|don't have a fever|do not have a fever|"
            r"not having a fever|without fever)\b", text, re.I
        ))
        positive_fever = bool(re.search(
            r"\bfever\b.*\b(?:for|since)\b|\bfever\b.*\bago\b",
            text, re.I
        ))

        if not (negative_fever and positive_fever):
            duration = re.search(
                r"\b(?:for|since|from)\s+(?:the\s+)?(?:last\s+|past\s+)?"
                r"(?:a week|one week|two weeks|three weeks|"
                r"\d+\s+(?:days?|weeks?|months?)|"
                r"yesterday|today|this morning|last night)\b"
                r"|\b(?:one week|a week|\d+\s+(?:days?|weeks?|months?))\s+ago\b",
                text, re.I
            )
            if duration:
                result["duration"] = duration.group(0).strip()

        allergy = re.search(
            r"\b(?:no known allergies|no allergies|no allergy|have not had any allerg(?:y|ies)|have no allerg(?:y|ies)|do not have any allerg(?:y|ies)|"
            r"not allergic to anything|nothing of allergy|"
            r"i (?:don't|do not) have (?:any )?allerg(?:y|ies))\b",
            text, re.I
        )
        if allergy:
            result["allergies"] = "No known allergies"
        else:
            allergy = re.search(
                r"\b(?:allergic to|allergy to)\s+([^,.!?;]+)",
                text, re.I
            )
            if allergy:
                result["allergies"] = allergy.group(1).strip()

        medication = re.search(
            r"\b(?:currently taking|taking medication(?:s)?(?: called)?|"
            r"my medication(?:s)? (?:is|are)|i take)\s+"
            r"([^,.!?;]+)",
            text, re.I
        )
        if medication:
            result["medications"] = medication.group(1).strip()

        return result

