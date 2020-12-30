import os
from datetime import datetime
from flask import Flask, jsonify, request, flash, redirect
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/images')
def set_images():
    if request.method == 'POST':
        folder = './images'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        files = request.files
        files = request.files.getlist("file[]")

        filename = ""
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('./images/', filename))


if __name__ == '__main__':
    CORS(app)
    app.run()

# Corro el algoritmo
# ejecutar()
