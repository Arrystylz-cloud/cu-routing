"""Building coordinate ingestion and validation."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = ("building_name", "latitude", "longitude")


def validate_schema(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def slugify_building_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower().strip())
    slug = re.sub(r"\s+", "-", slug)
    return re.sub(r"-+", "-", slug).strip("-")


def validate_coordinates(latitudes: Iterable[float], longitudes: Iterable[float]) -> None:
    for index, (lat, lon) in enumerate(zip(latitudes, longitudes)):
        if not (-90 <= float(lat) <= 90):
            raise ValueError(f"Invalid latitude at row {index}: {lat}")
        if not (-180 <= float(lon) <= 180):
            raise ValueError(f"Invalid longitude at row {index}: {lon}")


def load_buildings_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_schema(df)
    validate_coordinates(df["latitude"], df["longitude"])
    df["building_id"] = df["building_name"].map(slugify_building_name)
    return df
