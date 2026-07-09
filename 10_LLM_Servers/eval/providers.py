from app.rag import RAGProviderConfig
import os

def get_fireworks_config() -> RAGProviderConfig:
    return RAGProviderConfig(
        name="fireworks",
        embedding_model_name=os.environ.get("FIREWORKS_EMBEDDING_MODEL", "accounts/fireworks/models/qwen3-embedding-8b"),
        chat_model=os.environ.get("FIREWORKS_CHAT_MODEL", "accounts/fireworks/models/gpt-oss-20b"),
        api_key=os.environ["FIREWORKS_API_KEY"],
        api_base="https://api.fireworks.ai/inference/v1",
        embedding_kwargs={
            "check_embedding_ctx_length": False,
            "dimensions": 4096,
        },
    )

def get_openai_config() -> RAGProviderConfig:
    return RAGProviderConfig(
        name="openai",
        embedding_model_name=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=os.environ.get("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
        api_key=os.environ["OPENAI_API_KEY"],
        api_base="https://api.openai.com/v1",
        embedding_kwargs={},
    )

def get_judge_llm():
    from ragas.llms import llm_factory

    return llm_factory.get_llm(
        model=os.environ.get("JUDGE_MODEL_NAME", "gpt-5.1-mini"),
        api_key=os.environ["JUDGE_API_KEY"],
    )