from flask import Flask, request
from environs import Env
from kenzie import uploading, search_files, downloading, zipping
from os import environ

env = Env()
env.read_env()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(environ.get("MAX_CONTENT_LENGTH")) ** 2


@app.post("/upload")
def upload():
    img_list = request.files.getlist('file')
    return uploading(img_list)


@app.get("/files", defaults={'extension': None})            
@app.get("/files/<extension>")
def get_files(extension):
    return search_files(extension) 
    

@app.get("/download/<file_name>")
def download(file_name):
    return downloading(file_name)


@app.get("/download-zip")
def download_zip():
    return zipping(request.args)
   
