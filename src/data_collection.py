"""Building coordinate ingestion and validation."""

from __future__ import annotations

import re
from typing import Iterable
from collections import defaultdict

import pandas as pd


REQUIRED_COLUMNS = ("building_name", "latitude", "longitude")


def validate_schema(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

slug_counts = defaultdict(int)
def slugify_building_name(name: str, existing_slugs=None) -> str:
    if existing_slugs is None:
        existing_slugs = set()
    
    """Convert to lowercase, remove special characters"""
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower().strip())
    """replace spaces with hyphens."""
    slug = re.sub(r"\s+", "-", slug)
    """replace multiple hyphens with a single one."""
    slug = re.sub(r"-+", "-", slug).strip("-")

    """Handles Duplicate"""
    unique_slug = slug
    counter = 2
    while unique_slug in existing_slugs:
        unique_slug = f"{slug}-{counter}"
        counter += 1

    existing_slugs.add(unique_slug)
    return unique_slug

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
