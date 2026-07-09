"""RAGAS scoring helpers for Activity 1."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from eval.generate_testset import run_ragas_sync

REQUIRED_ROW_KEYS = (
    "user_input",
    "reference",
    "reference_contexts",
    "retrieved_contexts",
    "response",
)

METRIC_NAMES = (
    "context_recall",
    "faithfulness",
    "answer_accuracy",
)

MAX_CONTEXT_CHARS = int(os.environ.get("RAGAS_MAX_CONTEXT_CHARS", "2000"))


def _trim_contexts(contexts: list[str], max_chars: int = MAX_CONTEXT_CHARS) -> list[str]:
    """Trim retrieved contexts so judge prompts stay within token limits."""
    return [str(context)[:max_chars] for context in contexts]


def _validate_rows(rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("No rows provided for scoring.")

    for index, row in enumerate(rows):
        missing = [key for key in REQUIRED_ROW_KEYS if key not in row]
        if missing:
            raise ValueError(f"Row {index} is missing required keys: {missing}")


def build_judge_llm():
    """Return a RAGAS judge LLM used for all metric scoring."""
    import asyncio

    load_dotenv()

    from ragas.llms import llm_factory

    client = OpenAI(api_key=os.environ["JUDGE_API_KEY"])
    judge = llm_factory(
        os.environ.get("JUDGE_MODEL_NAME", "gpt-4.1-mini"),
        provider="openai",
        client=client,
        max_tokens=4096,
    )
    judge.model_args = {"max_tokens": 4096, "max_retries": 3}

    async def agenerate_from_sync(prompt, response_model):
        return await asyncio.to_thread(
            judge.generate,
            prompt=prompt,
            response_model=response_model,
        )

    judge.agenerate = agenerate_from_sync
    return judge


def build_rag_metrics(judge_llm):
    """Create the Activity 1 RAGAS metric set."""
    from ragas.metrics.collections import (
        AnswerAccuracy,
        ContextRecall,
        Faithfulness,
    )

    return {
        "context_recall": ContextRecall(llm=judge_llm),
        "faithfulness": Faithfulness(llm=judge_llm),
        "answer_accuracy": AnswerAccuracy(llm=judge_llm),
    }


async def score_rag_rows(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """Score RAG pipeline rows with ContextRecall, Faithfulness, and AnswerAccuracy."""
    _validate_rows(rows)

    judge_llm = build_judge_llm()
    metrics = build_rag_metrics(judge_llm)

    score_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        retrieved_contexts = _trim_contexts(row["retrieved_contexts"])
        score_rows.append(
            {
                "case": index,
                "context_recall": (
                    await metrics["context_recall"].ascore(
                        user_input=row["user_input"],
                        retrieved_contexts=retrieved_contexts,
                        reference=row["reference"],
                    )
                ).value,
                "faithfulness": (
                    await metrics["faithfulness"].ascore(
                        user_input=row["user_input"],
                        response=row["response"],
                        retrieved_contexts=retrieved_contexts,
                    )
                ).value,
                "answer_accuracy": (
                    await metrics["answer_accuracy"].ascore(
                        user_input=row["user_input"],
                        response=row["response"],
                        reference=row["reference"],
                    )
                ).value,
            }
        )

    return pd.DataFrame(score_rows)


def score_rag_rows_sync(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """Jupyter-safe sync wrapper around `score_rag_rows`."""
    import asyncio

    def invoke() -> pd.DataFrame:
        return asyncio.run(score_rag_rows(rows))

    return run_ragas_sync(invoke)


def summarize_scores(scores_df: pd.DataFrame) -> pd.Series:
    """Return mean score for each metric."""
    numeric_cols = [col for col in METRIC_NAMES if col in scores_df.columns]
    return scores_df[numeric_cols].mean(numeric_only=True)


def compare_providers(
    fireworks_scores: pd.DataFrame,
    openai_scores: pd.DataFrame,
) -> pd.DataFrame:
    """Return a side-by-side mean metric comparison."""
    comparison = pd.concat(
        [
            summarize_scores(fireworks_scores).rename("fireworks"),
            summarize_scores(openai_scores).rename("openai"),
        ],
        axis=1,
    )
    return comparison
