from flask import Flask, request, jsonify
from environs import Env
from kenzie import uploading, search_files, downloading, zipping
import os

env = Env()
env.read_env()

app = Flask(__name__)

@app.post("/upload")
def upload():
    max_size = os.environ.get("MAX_CONTENT_LENGTH")
    app.config['MAX_CONTENT_LENGTH'] = int(max_size) ** 2
    file_dir = os.environ.get("FILES_DIRECTORY")
    extensions = os.environ.get("ALLOWED_EXTENSIONS").split()
    output = ""

    if os.path.isdir("./images") == False:
        os.system(f"mkdir ./{file_dir}")
        os.system(f"touch img_files.txt")
        for ext in extensions:
            os.system(f"mkdir ./{file_dir}/{ext}")

    img_list = request.files.getlist('file')
    
    for img in img_list:
        if img and img.filename != "":
            file_extension = img.filename[-3:]

            if file_extension not in extensions:
                output = {'msg': "O formato da imagem é inválido"}, 415
            else:
                output = uploading(img, file_dir, file_extension)

    return output


@app.get("/files", defaults={'extension': None})            
@app.get("/files/<extension>")
def get_files(extension):
    extensions = os.environ.get("ALLOWED_EXTENSIONS").split()
    the_imgs = []
    
    for ext in extensions:
        for dirpath, dirnames, filenames in os.walk(f"./images/{str(ext)}"):
            if filenames != []:
                for img_name in filenames:
                    if img_name != ".DS_Store":
                        the_imgs.append({'name': img_name})
            else:
                return {'msg': "Lista vazia. Faça upload."}, 400

    if extension:
        return search_files(the_imgs, extension)
    else:
        return jsonify(the_imgs), 200


@app.get("/download/<file_name>")
def download(file_name):
    return downloading(file_name)


@app.get("/download-zip")
def download_zip():
    file_extension = request.args.get("file_extension").lower()
    compression_ratio = request.args.get("compression_ratio")
    return zipping(file_extension, compression_ratio)
   