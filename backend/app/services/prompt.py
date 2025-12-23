def build_prompt(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)

    return f"""
You are a SaaS support assistant.

Answer ONLY using the information below.
If the answer is not present, say:
"I do not have enough information to answer this."

Context:
{context}

Question:
{question}

Answer:
""".strip()
