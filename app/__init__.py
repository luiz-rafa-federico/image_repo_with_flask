from flask import Flask, request, jsonify
from environs import Env
from http import HTTPStatus
from kenzie import uploading, search_files, downloading, zipping
import os

env = Env()
env.read_env()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get("MAX_CONTENT_LENGTH")) ** 2
extensions = os.environ.get("ALLOWED_EXTENSIONS").split()
file_dir = os.environ.get("FILES_DIRECTORY")


@app.post("/upload")
def upload():
    img_list = request.files.getlist('file')
    return uploading(img_list)


@app.get("/files", defaults={'extension': None})            
@app.get("/files/<extension>")
def get_files(extension):
    the_imgs = []
    
    for ext in extensions:
        for dirpath, dirnames, filenames in os.walk(f"./{file_dir}/{str(ext)}"):
            if filenames != []:
                for img_name in filenames:
                    if img_name != ".DS_Store":
                        the_imgs.append({'name': img_name})
            else:
                return {'msg': "Lista vazia. Faça upload"}, HTTPStatus.NOT_FOUND

    if extension:
        return search_files(the_imgs, extension)
    else:
        return jsonify(the_imgs), HTTPStatus.OK


@app.get("/download/<file_name>")
def download(file_name):
    return downloading(file_name)


@app.get("/download-zip")
def download_zip():
    extension = request.args.get("file_extension")
    ratio = request.args.get("compression_ratio")
    return zipping(extension, ratio)
   
