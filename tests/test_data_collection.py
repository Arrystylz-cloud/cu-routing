import pandas as pd

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
