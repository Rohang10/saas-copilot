UNSAFE_KEYWORDS = [
    "medical advice",
    "legal advice",
    "diagnose",
    "prescription",
    "lawsuit",
    "personal data",
    "password",
]

def is_unsafe_question(question: str) -> bool:
    q = question.lower()
    return any(word in q for word in UNSAFE_KEYWORDS)
