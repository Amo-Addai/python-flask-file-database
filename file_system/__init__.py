import os

UPLOAD_FOLDER = "/uploads"


class FileSystem:
    def __init__(self):
        pass

    def setup_file_system(self, app):
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        return app

    def save_file(self, file, extra):
        file.save(os.path.join(UPLOAD_FOLDER, extra['filename'] if ('filename' in extra) else 'file'))
