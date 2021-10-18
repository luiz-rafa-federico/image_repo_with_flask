import os
from flask import jsonify, send_from_directory

def writing(file_name):
    with open("img_files.txt", "a") as f:
        f.write(file_name)
        f.write("\n")


def uploading(img, dir, extension):
    
    with open("img_files.txt", "r") as f:
        for line in f:
            if img.filename.lower() in line:
                return {'msg': "O nome do arquivo já existe."}, 409

    img.save(f"./{dir}/{extension}/{img.filename.lower()}")
    writing(img.filename.lower())
    
    return {'msg': f"Upload concluído com sucesso"}, 201
    

def search_files(images, extension):
    filtered = [pic for pic in images if extension.lower() in pic['name']]
    if filtered:
        return jsonify(filtered), 200
    else:
        return {'msg': "Arquivos não encontrados"}, 400


def downloading(file_name):
    allowed_extensions = ["png", "jpg", "gif"]
    if file_name[-3:].lower() in allowed_extensions:
        return send_from_directory(f"../images/{file_name[-3:]}", path=f"{file_name}", as_attachment=True), 200
    else:
        return {'msg': "Imagem não encontrada."}, 404


def zipping(extension, ratio):
    allowed_extensions = ["png", "jpg", "gif"]
    dir_path = f"../images/{str(extension)}"
    
    if extension in allowed_extensions:
        zip_files = os.popen(f"zip photos -r {dir_path}")
        return send_from_directory("/tmp", path="photos.zip", as_attachment=True), 200
    else:
        return {'msg': "Imagens não encontradas"}, 404