from flask import Flask
import server

app = Flask(__name__)
app = server.setup_db(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/uploads/<path:filename>', methods=["POST"])
def handle_upload(filename):
    if server.handle_file(request.files["file"], extra):
        pass
    else:
        return 'Sorry, something went wrong'

if __name__ == '__main__':
    app.run()
