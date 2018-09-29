import os

UPLOAD_FOLDER = "/uploads"


def setup_file_system(app):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return app


def save_file(file, extra):
    file.save(os.path.join(UPLOAD_FOLDER, extra['filename'] if ('filename' in extra) else 'file'))
