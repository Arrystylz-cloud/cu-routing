"""CSV export helpers for routing artifacts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_dataframe(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
