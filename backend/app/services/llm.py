import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set in environment variables")

client = Groq(api_key=api_key)
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise SaaS support assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
