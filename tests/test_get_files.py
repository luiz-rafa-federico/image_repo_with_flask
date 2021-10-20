def test_if_file_route_exists(app_routes):
    assert app_routes.match("/files"), "Verifique se há uma rota '/files'"


def test_if_file_unique_route_exists(app_routes):
    assert app_routes.match("/files<extension>"), "Verifique se há uma rota '/files<extension>'"