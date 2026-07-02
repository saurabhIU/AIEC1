from __future__ import annotations

import os

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

DEFAULT_CHAT_MODEL = "gpt-5.4-mini"


def get_chat_model(model_name: str | None = None, *, temperature: float = 0) -> ChatOpenAI:
    name = model_name or os.environ.get("RAG_MODEL_NAME", DEFAULT_CHAT_MODEL)
    return ChatOpenAI(
        model=name,
        temperature=temperature,
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )

def get_judge_model(model_name: str | None = None, *, temperature: float = 0) -> ChatOpenAI:
    name = model_name or os.environ.get("JUDGE_MODEL_NAME", DEFAULT_CHAT_MODEL)
    return ChatOpenAI(
        model=name,
        temperature=temperature,
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )
