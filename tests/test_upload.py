from werkzeug.datastructures import FileStorage
from app import app

test_client = app.test_client()

def test_if_upload_route_accepts_post_request():
    assert 'POST' in (test_client.options('/upload').headers['Allow'])


def test_if_upload_route_does_not_accept_get_request():
    assert 'GET' not in (test_client.options('/upload').headers['Allow'])
    assert test_client.get('/upload').status_code == 405


def test_if_upload_route_using_form_returns_code_200_if_successful():
    FILE_PATH = './images/gif/kenzie.gif'
    with open(FILE_PATH, 'rb') as file:
        my_file = FileStorage(stream=file, filename='test.gif', content_type='image/gif')
        response = test_client.post('/upload', data={"file1": my_file}, content_type="multipart/form-data")
        assert response.status_code == 200


def test_if_there_is_a_file_in_images_gif_directory():
    from os import path
    filepath = './images/gif/kenzie.gif'
    assert path.isfile(filepath)


# def test_file_upload_using_form_creates_file_in_directory_if_successful():
#     FILE_PATH = './images/gif/kenzie.gif'
#     with open(FILE_PATH, 'rb') as file:
#         from datetime import datetime
#         new_filename = f"{str(datetime.utcnow()).split('.')[-1]}.gif"
#         test_file = FileStorage(stream=file, filename=new_filename, content_type='image/gif')
#         response = test_client.post('/upload', data={"file1": test_file}, content_type="multipart/form-data")
#         assert response.status_code == 200

#         from os import path
#         filepath = f'./images/gif/{new_filename}'
#         assert path.isfile(filepath)