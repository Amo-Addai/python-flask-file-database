from flaskext.mysql import MySQL

mysql = MySQL()


class MySQLDatabase:

    def __init__(self):
        pass

    def setup_mysql_db(self, app):  # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = ''
        app.config['MYSQL_DATABASE_DB'] = 'roytuts'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
