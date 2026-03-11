import pandas as pd

from src.data_collection import slugify_building_name, validate_coordinates, validate_schema


def test_slugify_building_name():
    assert slugify_building_name("Engineering Auditorium") == "engineering-auditorium"


def test_validate_schema_passes():
    df = pd.DataFrame(columns=["building_name", "latitude", "longitude"])
    validate_schema(df)


def test_validate_coordinates_passes():
    validate_coordinates([6.67], [3.15])
