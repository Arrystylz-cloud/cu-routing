import pandas as pd
import pytest

from src.data_collection import slugify_building_name, validate_coordinates, validate_schema, load_buildings_csv


def test_slugify_building_name():
    existing = set()
    assert slugify_building_name("Engineering Auditorium", existing) == "engineering-auditorium"


def test_validate_schema_passes():
    df = pd.DataFrame(columns=["building_name", "latitude", "longitude"])
    validate_schema(df)

def test_slugify_special_chars():
    existing = set()
    assert slugify_building_name("Engineering @ Auditorium!", existing) == "engineering-auditorium"

def test_slugify_spaces():
    existing = set()
    assert slugify_building_name("Engineering   Auditorium", existing) == "engineering-auditorium"

def test_slugify_duplicates():
    existing = set()
    # First occurrence
    assert slugify_building_name("Engineering Auditorium", existing) == "engineering-auditorium"
    # Second occurrence
    assert slugify_building_name("Engineering Auditorium", existing) == "engineering-auditorium-2"
    # Third occurrence
    assert slugify_building_name("Engineering Auditorium", existing) == "engineering-auditorium-3"

def test_validate_coordinates_passes():
    validate_coordinates([6.67], [3.15])

def test_load_buildings_csv(tmp_path):
    csv = tmp_path / "buildings.csv"

    csv.write_text(
        """building_name,latitude,longitude
Engineering Auditorium,10,20
Engineering  Auditorium,11,21
Engineering @ Auditorium!,12,22
"""
    )

    df = load_buildings_csv(csv)

    assert list(df["building_id"]) == [
        "engineering-auditorium",
        "engineering-auditorium-2",
        "engineering-auditorium-3",
    ]



def test_slugify_empty_name_raises():
    existing = set()
    with pytest.raises(ValueError):
        slugify_building_name("!!!", existing)


def test_slugify_non_string_raises():
    existing = set()
    with pytest.raises(ValueError):
        slugify_building_name(None, existing)


def test_validate_coordinates_invalid_latitude():
    with pytest.raises(ValueError):
        validate_coordinates([100], [0])


def test_validate_coordinates_invalid_longitude():
    with pytest.raises(ValueError):
        validate_coordinates([0], [200])


def test_load_buildings_csv_missing_name_raises(tmp_path):
    csv = tmp_path / "buildings.csv"

    csv.write_text(
        """building_name,latitude,longitude
Engineering Auditorium,10,20
,11,21
"""
    )

    with pytest.raises(ValueError):
        load_buildings_csv(csv)