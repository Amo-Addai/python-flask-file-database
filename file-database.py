from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from server import Server

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv', 'json',
                          'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
server = Server()
app = server.setup_db_and_file_system(app)
print("Server, Database, and File System have all been set up successfully!!")
print()


def allowed_files(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST':  # and request.form:
        extra = {
            'body': request.form
        }
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
        file_is_allowed, extra["file_type"] = allowed_files(file.filename)
        if file and file_is_allowed:
            filename = secure_filename(file.filename)
            print("Now handling file '{}'".format(filename))
            extra["filename"] = filename
            if server.handle_file(file, extra):
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
