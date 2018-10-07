from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from server import Server

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv', 'json', 'xml', 'txt', 'pdf'])
CATEGORIES = set([])

app = Flask(__name__)
server = Server()
app = server.setup_db_and_file_system(app)
print("Server, Database, and File System have all been set up successfully!!")
print()
default_filter, default_category, default_collection, default_filename, default_file_type = "all", "All", "Examination", "", ""


def allowed_files(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


def render_home():
    return render_template('home.html', ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS)


@app.route('/')
def home():
    return render_home()


@app.route('/collections', methods=['GET'])
def get_collections_data():
    query = request.args if (request.args is not None) else {"category": "All"}
    if ("category" not in query) or (len(query["category"]) <= 0):
        query["category"] = "all"
    print("QUERY -> {}".format(query))
    return server.get_collections(query)


@app.route('/request', methods=['GET', 'POST'])
def request_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST':  # and request.form:
        extra = {
            'body': request.form
        }  # FIND A WAY TO ASSIGN THE THESE PARAMS GENERICALLY
        extra["filter"] = default_filter if (
            ("filter" not in extra["body"]) or (len(extra["body"]["filter"]) <= 0)) else extra["body"]["filter"]
        extra["collection"] = default_collection if (
            ("collection" not in extra["body"]) or (len(extra["body"]["collection"]) <= 0)) else extra["body"][
            "collection"]
        extra["category"] = default_category if (
            ("category" not in extra["body"]) or (len(extra["body"]["category"]) <= 0)) else extra["body"][
            "category"]
        extra["filename"] = default_filename if (
            ("filename" not in extra["body"]) or (len(extra["body"]["filename"]) <= 0)) else extra["body"]["filename"]
        extra["file_type"] = default_file_type if (
            ("file_type" not in extra["body"]) or (len(extra["body"]["file_type"]) <= 0)) else extra["body"][
            "file_type"]
        filename, filter = secure_filename(extra["filename"]), extra["body"]["filter"]
        print("Now requesting file '{}'".format(filename))
        print("With parameters -> {}".format(extra))
        file = server.request_file(filter, extra)
        if file is not None:
            print("Server handled file-request '{}' successfully -> {}".format(filename, file))
            # FIND A WAY TO PUT THE file WITHIN THE CLIENT'S UI, FOR USER TO DOWNLOAD IT
        else:
            print("Server could not handle file-request '{}' successfully".format(filename))
        return render_home()
    return render_home()


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    if request.method == 'POST':  # and request.form:
        extra = {
            'body': request.form
        }  # FIND A WAY TO ASSIGN THE THESE PARAMS GENERICALLY
        extra["collection"] = default_collection if (
            ("collection" not in extra["body"]) or (len(extra["body"]["collection"]) <= 0)) else extra["body"][
            "collection"]
        extra["category"] = default_category if (
            ("category" not in extra["body"]) or (len(extra["body"]["category"]) <= 0)) else extra["body"][
            "category"]
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return render_home()
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return render_home()
        file_is_allowed, extra["file_type"] = allowed_files(file.filename)
        if file and file_is_allowed:
            filename = secure_filename(file.filename)
            print("Now handling file '{}'".format(filename))
            extra["filename"] = filename  # FIND A WAY TO ASSIGN THE COLLECTION GENERICALLY
            if server.handle_file(file, extra):
                print("Server handled file '{}' successfully.".format(filename))
            else:
                print("Server could not handle file '{}' successfully".format(filename))
        return render_home()
    return render_home()


if __name__ == '__main__':
    app.run()
