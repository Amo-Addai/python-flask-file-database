from flask import Flask, flash, request, redirect, url_for
import server
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads/folder'
ALLOWED_EXTENSIONS = set(['xls', 'csv', 'json',
                          'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app = server.setup_db(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Hello World!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():  #   FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST' and request.body:
        body = request.body
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if server.handle_file(filename, file, body):
                #   DECIDE WHETHER TO SAVE THIS FILE IN THE UPLOAD FOLDER OR NOT 1ST!!!
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file', filename=filename))
            else:
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
