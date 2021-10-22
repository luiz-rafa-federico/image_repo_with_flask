from app import app
import pytest

test_client = app.test_client()

def test_if_download_route_exists(app_routes):
    assert app_routes.match("/download/<file_name>"), "Verifique se há uma rota '/download/<file_name>'"


def test_if_download_unique_file_route_does_not_accept_post_request():
    assert 'POST' not in (test_client.options('/download/<file_name>').headers['Allow'])
    assert test_client.post('/download/<file_name>').status_code == 405


def test_if_download_unique_file_route_accepts_get_request():
    assert 'GET' in (test_client.options('/download/<file_name>').headers['Allow'])


def test_if_download_unique_file_receives_a_non_accepted_parameter_type():
    with pytest.raises(TypeError):
        from app import download
        download(5)


def test_if_download_zip_route_exists(app_routes):
    assert app_routes.match("/download-zip"), "Verifique se há uma rota '/download-zip'"


def test_if_download_zip_function_receives_a_non_accepted_positional_argument():
    with pytest.raises(TypeError):
        from app import download_zip
        download_zip("5")
    
