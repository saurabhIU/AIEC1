"""Run a RAG graph over an evaluation test set."""

from __future__ import annotations

from typing import Any

import pandas as pd


def as_context_list(value: Any) -> list[str]:
    """Normalize a CSV cell or list value into a list of context strings."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    text = str(value).strip()
    return [text] if text else []


def run_rag_over_testset(graph, testset_df: pd.DataFrame) -> list[dict[str, Any]]:
    """Invoke the RAG graph for each test row and return RAGAS-ready records.

    Each returned row should include:
    - user_input
    - reference
    - reference_contexts
    - retrieved_contexts
    - response
    """
    rows: list[dict[str, Any]] = []

    for _, row in testset_df.iterrows():
        result = graph.invoke({"question": row["user_input"]})

        retrieved_contexts = [
            doc.page_content
            for doc in result.get("context", [])
        ]

        rows.append(
            {
                "user_input": row["user_input"],
                "reference": row["reference"],
                "reference_contexts": as_context_list(row["reference_contexts"]),
                "retrieved_contexts": retrieved_contexts,
                "response": result["response"],
            }
        )

    return rows
