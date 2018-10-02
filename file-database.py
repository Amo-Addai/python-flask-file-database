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
import os


def allowed_files(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/request', methods=['GET', 'POST'])
def request_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST':  # and request.form:
        extra = {
            'body': request.form
        }  # FIND A WAY TO ASSIGN THE THESE PARAMS GENERICALLY
        extra["body"]["filter"] = "all" if ("filter" not in extra["body"]) else extra["body"]["filter"]
        extra["table"] = "Examination" if ("table" not in extra["body"]) else extra["body"]["table"]
        extra["filename"] = "default" if ("filename" not in extra["body"]) else extra["body"]["filename"]
        extra["file_type"] = "default" if ("file_type" not in extra["body"]) else extra["body"]["file_type"]
        filename, filter = secure_filename(extra["filename"]), extra["body"]["filter"]
        print("Now requesting file '{}'".format(filename))
        print("With parameters -> {}".format(extra))
        file = server.request_file(filter, extra)
        if file is not None:
            print("Server handled file-request '{}' successfully -> {}".format(filename, file))
            # FIND A WAY TO PUT THE file WITHIN THE CLIENT'S UI, FOR USER TO DOWNLOAD IT
        else:
            print("Server could not handle file-request '{}' successfully".format(filename))
        return redirect(request.url)
    return '''
    PUT THE HTML CODE RIGHT HERE ...
    '''


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
            extra["filename"], extra["table"] = filename, "Examination"  # FIND A WAY TO ASSIGN THE TABLE GENERICALLY
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
