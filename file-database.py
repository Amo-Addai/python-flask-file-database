from flask import Flask, request, render_template, Response, send_file, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import json, os

from server import Server

ALLOWED_EXTENSIONS = set(['csv', 'tsv', 'xls', 'xlsx', 'html', 'xml', 'sql', 'json', 'txt', 'pdf'])
CATEGORIES = set(['All'])

# os.path.join(current_directory, "/server/downloads/") OR os.getcwd()
current_directory = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_FOLDER = current_directory + "/server/downloads/"
# print(DOWNLOAD_FOLDER)  # 'C:\Users\kwadw\Desktop\file-database/server/downloads/

app = Flask(__name__)
server = Server()
app = server.setup_db_and_file_system(app)
print("Server, Database, and File System have all been set up successfully!!")
print()
default_filter, default_category, default_collection, default_filename, default_file_type = None, "All", "Examination", "", ""
request_data, response_message, response_data = {}, "Sorry, some error occurred.", {}


def get_request_data():
    global request_data
    data = request_data
    request_data = {}
    return data


def get_response_message():
    global response_message
    msg = response_message
    response_message = "Sorry, some error occurred."
    return msg


def get_response_data():
    global response_data
    data = response_data
    response_data = {}
    return data


def allowed_files(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


def return_response(success):
    global response_message, response_data
    final_data = {'success': success, 'message': get_response_message(), 'data': get_response_data()}
    print()
    print("NOW, RETURN RESPONSE -> {}".format(final_data))
    response = app.response_class(
        response=json.dumps(final_data),
        status=200 if success else 300,
        mimetype='application/json'
    )
    return response


def render_home():
    return render_template('home.html', ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS, CATEGORIES=CATEGORIES)


@app.route('/')
def home():
    return render_home()


@app.route('/api/collections', methods=['GET'])
def get_collections_data():
    global request_data, response_message, response_data
    query = request.args if (request.args is not None) else {"category": "All"}
    if ("category" not in query) or (len(query["category"]) <= 0):
        query["category"] = "All"
    print("QUERY -> {}".format(query))
    response_data = server.get_collections(query)
    if response_data is not None:
        response_message = "Collections Available" if (len(response_data) > 0) else "No Collections Available"
    return return_response(True)


@app.route('/api/collections', methods=['DELETE'])
def delete_collection_data():
    global request_data, response_message, response_data
    if request.method == 'DELETE':
        request_data, extra = request.args, {}
        print("REQUEST -> {}".format(request_data))
        extra["category"] = default_category if (
            ("category" not in request_data) or (len(request_data["category"]) <= 0)) else request_data[
            "category"]
        if "_id" in request_data:
            extra["_id"] = request_data["_id"]
            if server.delete_collection(extra):
                response_message = "Collection deleted successfully"
                return return_response(True)
            response_message = "Collection could not be deleted successfully"
        response_message = "Collection not selected correctly"
    return return_response(False)


@app.route('/api/collections/upload', methods=['POST'])
def upload_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    global request_data, response_message, response_data
    if request.method == 'POST':
        request_data, extra = request.form, {}
        print("REQUEST -> {}".format(request_data))
        extra["category"] = default_category if (
            ("category" not in request_data) or (len(request_data["category"]) <= 0)) else request_data[
            "category"]
        extra["collection"] = default_collection if (
            ("collection" not in request_data) or (len(request_data["collection"]) <= 0)) else request_data[
            "collection"]
        extra["filename"] = default_filename if (
            ("filename" not in request_data) or (len(request_data["filename"]) <= 0)) else request_data["filename"]
        #
        if 'file' not in request.files:
            response_message = "No file within data"
            return return_response(False)
        file = request.files['file']
        if file.filename == '':
            response_message = "No selected file"
            return return_response(False)
        file_is_allowed, extra["file_type"] = allowed_files(extra["filename"])
        #
        if file and file_is_allowed:
            filename = extra["filename"] = secure_filename(extra["filename"])
            print("Now handling file '{}' -> {}".format(filename, file))
            print("With params -> {}".format(extra))
            if server.handle_file(file, extra):
                response_message, response_data = "Server handled file '{}' successfully.".format(filename), {
                    # FIGURE OUT WHAT RESPONSE DATA TO PUT IN HERE :)
                }
                return return_response(True)
            else:
                response_message = "Server could not handle file '{}' successfully.".format(filename)
        return return_response(False)
    return return_response(False)


@app.route('/api/collections/download', methods=['PUT'])
def request_file():  # FIND THE RIGHT WAY TO RETRIEVE request.body
    global request_data, response_message, response_data
    if request.method == 'PUT':
        request_data, extra = request.json, {}
        print("REQUEST -> {}".format(request_data))
        extra["category"] = default_category if (
            ("category" not in request_data) or (len(request_data["category"]) <= 0)) else request_data[
            "category"]
        extra["collection"] = default_collection if (
            ("collection" not in request_data) or (len(request_data["collection"]) <= 0)) else request_data[
            "collection"]
        extra["filename"] = default_filename if (
            ("filename" not in request_data) or (len(request_data["filename"]) <= 0)) else request_data["filename"]
        extra["file_type"] = default_file_type if (
            ("file_type" not in request_data) or (len(request_data["file_type"]) <= 0)) else request_data[
            "file_type"]
        extra["filter"] = default_filter if (
            ("filter" not in request_data) or (len(request_data["filter"]) <= 0)) else request_data["filter"]
        #
        filename, file_type, filter = extra["filename"], extra["file_type"], extra["filter"]
        print("Now requesting file '{}'".format(filename))
        print("With parameters -> {}".format(extra))
        filepath, filename = server.request_file(filter, extra)
        if (filepath is not None) and (filename is not None):
            response_message, response_data = "Server handled file-download request '{}' successfully".format(
                filename), {"filename": filename}
            print("Now attempting to send file '{}' to client for download -> {}".format(filename, filepath))
            return return_response(True)
        else:
            response_message = "Server could not handle file-download request '{}' successfully".format(filename)
        return return_response(False)
    return return_response(False)


@app.route('/api/collections/download/file', methods=['POST'])
def download_file():
    global request_data, response_message, response_data
    if request.method == 'POST':
        request_data, extra = request.form, {}
        print("REQUEST DATA -> {}".format(request_data))
        try:
            if "filename" in request_data:
                filename = request_data["filename"]
                if len(filename) > 0:
                    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True,
                                               attachment_filename=filename)
                    # return send_file("{}{}".format(DOWNLOAD_FOLDER, filename), as_attachment=True, attachment_filename=filename,
                    #                  mimetype='application/octet-stream')
                    # return Response('data comes here', mimetype='application/octet-stream',
                    #                  headers={"Content-disposition": "attachment; filename{}".format(filename)})
                response_message = "Server could not provide download file '{}' successfully".format(filename)
        except Exception as e:
            print("ERROR -> {}".format(e))
    return return_response(False)


if __name__ == '__main__':
    app.run()
