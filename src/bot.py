"""
Application Under Test (AUT): Customer Support RAG Bot
------------------------------------------------------
This module implements the live RAG application:
1. Document Retrieval: Fetches relevant policy snippets from store_policies.json.
2. Answer Generation: Calls Google Gemini with retrieved context and system guardrails.
3. Response Object: Returns answer text and retrieved chunks for DeepEval evaluation.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from google import genai
from dotenv import load_dotenv

# Ensure environment is loaded
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


@dataclass
class BotResponse:
    """Standardized response container returned by the RAG Bot."""
    answer: str
    retrieved_chunks: List[str]
    model_used: str


class CustomerSupportRAGBot:
    """Live Customer Support RAG Bot powered by Google Gemini."""

    def __init__(
        self,
        knowledge_base_path: Optional[Path] = None,
        model_name: Optional[str] = None,
    ):
        self.kb_path = (
            knowledge_base_path
            or Path(__file__).parent / "knowledge_base" / "store_policies.json"
        )
        self.model_name = (
            model_name
            or os.getenv("GEMINI_MODEL_NAME", "gemini-3.5-flash-lite")
        )
        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")

        self.client = genai.Client(api_key=self.api_key)
        self.documents = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[dict]:
        """Loads company policy documents from JSON."""
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """
        Retrieves the top_k most relevant policy snippets based on keyword scoring.
        """
        query_words = set(re.findall(r"\w+", query.lower()))
        scored_docs = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            topic_lower = doc["topic"].lower()

            # Score matching words in topic and content
            topic_matches = sum(1 for word in query_words if word in topic_lower)
            content_matches = sum(1 for word in query_words if word in content_lower)

            score = (topic_matches * 3) + content_matches
            scored_docs.append((score, doc["content"]))

        # Sort descending by score
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        # Return top_k document chunks (or all if fewer available)
        return [content for _, content in scored_docs[:top_k]]

    def query(self, user_query: str) -> BotResponse:
        """
        Executes end-to-end RAG: retrieves relevant chunks, crafts the prompt,
        and generates a response using Google Gemini.
        """
        retrieved_chunks = self.retrieve(user_query, top_k=2)
        context_str = "\n\n".join(
            f"[Document Chunk {i+1}]: {chunk}"
            for i, chunk in enumerate(retrieved_chunks)
        )

        prompt = f"""You are Nova, an empathetic and professional customer support assistant for an online store.
Answer the customer's question based strictly on the provided company policy documents.

COMPANY POLICY CONTEXT:
{context_str}

GUIDELINES:
- Answer the customer's question directly, clearly, and concisely in the very first sentence.
- Avoid unnecessary opening conversational filler, polite ramblings, or repetitive closing sign-offs.
- If the customer expresses frustration, briefly validate their feelings with empathy before providing the direct answer.
- Base your answers STRICTLY on the policy documents above. If the information is not in the documents, state that you do not have that specific information.
- Do not invent facts, warranty terms, or fees.

CUSTOMER QUESTION:
{user_query}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        answer_text = response.text.strip() if response.text else ""

        return BotResponse(
            answer=answer_text,
            retrieved_chunks=retrieved_chunks,
            model_used=self.model_name,
        )
