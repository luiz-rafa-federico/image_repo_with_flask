import os
from typing import Text
from uuid import uuid4
from http import HTTPStatus
from flask import jsonify, send_from_directory

FILE_DIR = os.environ.get("FILES_DIRECTORY")
EXTENSIONS = str(os.environ.get("ALLOWED_EXTENSIONS")).split()

def uploading(images):
    output = ""
    img_names = []

    if not os.path.isdir(f"./{FILE_DIR}"):
        os.system(f"mkdir ./{FILE_DIR}")
        for ext in EXTENSIONS:
            os.system(f"mkdir ./{FILE_DIR}/{ext}")

    for img in images:
        if img and img.filename != "":
            file_extension = img.filename[-3:]
            img_names.append(img.filename)

            if file_extension not in EXTENSIONS:
                output = {'msg': "O formato da imagem é inválido"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            elif img.filename.lower() in os.listdir(f"./{FILE_DIR}/{file_extension}"):
                output= {'msg': "O nome do arquivo já existe"}, HTTPStatus.CONFLICT
            else:
                img.save(f"./{FILE_DIR}/{file_extension}/{img.filename.lower()}")
                output = {'msg': f"Upload de {img_names} concluído com sucesso"}, HTTPStatus.CREATED
    return output
    

def search_files(extension):
    the_imgs = []
    output = ""
    
    for ext in EXTENSIONS:
        for _, _, filenames in os.walk(f"./{FILE_DIR}/{str(ext)}"):
            if filenames != []:
                for img_name in filenames:
                    the_imgs.append({'name': img_name})
            else:
                output = {'msg': "Lista vazia. Faça upload"}, HTTPStatus.NOT_FOUND

    if not extension:
        output = jsonify(the_imgs), HTTPStatus.OK
    else:
        filtered = [pic for pic in the_imgs if extension.lower() in pic['name']]
        if filtered:
            output = jsonify(filtered), HTTPStatus.OK
        else:
            output = {'msg': "Arquivos não encontrados"}, HTTPStatus.NOT_FOUND
    
    return output


def downloading(file_name):
    if file_name[-3:].lower() in EXTENSIONS:
        return send_from_directory(f"../{FILE_DIR}/{file_name[-3:]}", path=f"{file_name}", as_attachment=True), HTTPStatus.OK
    else:
        return {'msg': "Imagem não encontrada"}, HTTPStatus.NOT_FOUND


def generate_random_name(l):
    import string, random
    letters = string.ascii_letters
    name = "".join(random.choice(letters) for _ in range(l))
    return name


def zipping(request):
    extension = request.get("file_extension")
    ratio = request.get("compression_ratio")
    dir_path = f"./{FILE_DIR}/{str(extension)}"

    if not os.listdir(dir_path):
        return {'msg': "A pasta está vazia"}, HTTPStatus.NOT_FOUND
    
    if extension.lower() in EXTENSIONS:
        random_name = generate_random_name(4)
        os.system(f"zip -r -{ratio} /tmp/{str(random_name.lower())} {dir_path}")
        return send_from_directory("/tmp", path=f"{str(random_name.lower())}.zip", as_attachment=True), HTTPStatus.OK
    else:
        return {'msg': "Imagens não encontradas"}, HTTPStatus.NOT_FOUND