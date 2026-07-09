"""Load and validate the RAG evaluation test set."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ("user_input", "reference", "reference_contexts")
DEFAULT_TESTSET_PATH = Path(__file__).resolve().parent / "testset.csv"


def validate_testset(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the test set has required columns and no empty questions."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Test set is missing required columns: {missing}")

    if df["user_input"].astype(str).str.strip().eq("").any():
        raise ValueError("Test set contains empty user_input values.")

    # TODO: reject rows that still contain REPLACE placeholders before running eval
    placeholder_mask = df["reference"].astype(str).str.startswith("REPLACE:")
    if placeholder_mask.any():
        raise ValueError(
            "Test set still has placeholder reference answers. "
            "Update eval/testset.csv with ground-truth answers from your PDFs."
        )

    return df.loc[:, list(REQUIRED_COLUMNS)].copy()


def load_testset(path: str | Path = DEFAULT_TESTSET_PATH) -> pd.DataFrame:
    """Load the evaluation CSV and validate its schema."""
    testset_path = Path(path)
    if not testset_path.exists():
        raise FileNotFoundError(
            f"Test set not found at {testset_path}. "
            "Create eval/testset.csv or pass a different path."
        )

    df = pd.read_csv(testset_path)
    return validate_testset(df)
