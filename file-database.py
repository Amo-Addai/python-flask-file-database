from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import server

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv', 'json',
                          'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app = server.setup_db_and_file_system(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST':  # and request.form:
        body = request.form
        print("BODY -> {}".format(body))
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            print("Now handling file '{}'".format(filename))
            if server.handle_file(filename, file, body):
                print("Server handled file '{}' successfully.".format(filename))
            else:
                print("Server could not handle file '{}' successfully".format(filename))
        return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
