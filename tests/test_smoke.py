def test_modules_import():
    import src.config
    import src.data_collection
    import src.export_csv
    import src.graph_builder
    import src.router

    assert src.config is not None
