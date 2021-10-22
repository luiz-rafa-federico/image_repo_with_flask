from app import app
from kenzie import image

def app_client():
    return app.test_client()

def test_if_file_route_exists(app_routes):
    assert app_routes.match("/files"), "Verifique se há uma rota '/files'"


def test_if_file_unique_route_exists(app_routes):
    assert app_routes.match("/files/<extension>"), "Verifique se há uma rota '/files<extension>'"


def test_if_get_files_function_returns_200_if_successful():
    client = app_client()
    response = client.get("/files")
    assert response.status_code == 200, "Verifique a rota. Não está retornando os arquivos criados"


def test_if_get_files_returns_a_list_if_successful():
    client = app_client()
    response = client.get("/files")
    assert type(response.get_json()) == list, "Não retornou uma lista"


def test_if_get_files_returns_a_dict_if_successful():
    client = app_client()
    response = client.get("/files/<extension>")
    assert type(response.get_json()) == dict, "Não retornou um dicionário"