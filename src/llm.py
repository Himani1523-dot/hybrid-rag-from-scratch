from openai import OpenAI
from config import LLM_BASE_URL, LLM_MODEL ,MAX_CONTEXT_CHARS, MAX_CHUNK_CHARS

from src.utils.logger import get_logger
logger = get_logger(__name__)


class LLM:
    def __init__(self):
        self.client = OpenAI(
            base_url=LLM_BASE_URL,
            api_key="not-needed"
        )

    def generate(self, query: str, context_chunks: list[dict]) -> str:
        """
        Generate answer using retrieved chunks
        """

        # context = "\n\n".join(
        #     [chunk["text"] for chunk in context_chunks]
        # )
        context = ""

        for chunk in context_chunks:
            chunk_text = chunk["text"][:MAX_CHUNK_CHARS]

            if len(context) + len(chunk_text) > MAX_CONTEXT_CHARS:
                break

            context += chunk_text + "\n\n"
        
        logger.debug("\n[DEBUG] CONTEXT SENT TO LLM:\n", context)

        prompt = f"""
        <|system|>
        You are a strict QA system.

       You are a strict QA system.

        Rules:
        - Answer using ONLY the provided context.
        - If the answer is clearly present, respond with a concise answer.
        - Prefer information from the most relevant section.
        - If the answer is not present, say:
        "I don't know based on the provided document."
        - Do NOT make up information.

        <|user|>
        Context:
        {context}

        Question: {query}

        <|assistant|>
        """
        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content