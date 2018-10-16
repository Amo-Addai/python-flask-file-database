from flaskext.mysql import MySQL
import pymysql

mysql = MySQL()
host, db_port, user, password, db = "localhost", 3306, "test", "password", "database_name"
TABLES = ["courses", "schedules", "venues"]


class MySQLDatabase:
    encryption = None, None
    conn, cursor = None, None

    def __init__(self):
        pass

    def setup_mysql_db(self, app):  # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_DB'] = db
        app.config['MYSQL_DATABASE_HOST'] = host
        mysql.init_app(app)
        #  EITHER OF THESE 2 WILL WORK :)
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()
        #
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                    cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4')
        self.cursor = self.conn.cursor()
        #
        return app

    def close_mysql_db(self):
        self.conn.close()  # DISCONNECT FROM THE DATABASE
        return True

    def roll_back(self):  # Rollback in case there is any error
        self.conn.rollback()

    def get_data(self, table, columns=None, query=None, limit=None):
        try:  # 1ST, FIND A WAY TO SETUP columns PARAM VERY WELL ..
            query = "SELECT {} FROM {}{}{}".format((columns if columns is not None else "*"), table,
                                                   (("  WHERE {}".format(query)) if query is not None else ""),
                                                   ((" LIMIT {}".format(limit)) if limit is not None else ""))
            print("QUERY -> '{}'".format(query))
            self.cursor.execute(query)
            result, data = self.cursor.fetchall(), []
            for row in result:
                print(row)
                data.append(row)
            return data
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

    def get_data_object(self, table, columns=None, query=None, limit=None):
        try:  # 1ST, FIND A WAY TO SETUP columns PARAM VERY WELL ..
            query = "SELECT {} FROM {}{}{}".format((columns if columns is not None else "*"), table,
                                                   (("  WHERE {}".format(query)) if query is not None else ""),
                                                   ((" LIMIT {}".format(limit)) if limit is not None else ""))
            print("QUERY -> '{}'".format(query))
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

    def insert_data_object(self, table, columns=None, data=[]):
        try:  # YOU CAN EXTRACT KEYS OF data FOR columns
            query = "INSERT INTO {} {} VALUES {}".format(table,
                                                         (("({})".format(columns)) if columns is not None else "(*)"),
                                                         ([]))
            # """INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
            print("QUERY -> '{}'".format(query))
            self.cursor.execute(query)
            result = {}  # self.cursor.fetchall()  # FIND A WAY TO RETURN BACK THE DATA THAT'S JUST BEEN SAVED WITHIN THE DB
            self.conn.commit()
            return result
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

    def update_data(self, table, columns=None, data=[]):
        try:
            query = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
            # "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
            print("QUERY -> '{}'".format(query))
            self.cursor.execute(query)
            result = {}  # self.cursor.fetchall()  # FIND A WAY TO RETURN BACK THE DATA THAT'S JUST BEEN SAVED WITHIN THE DB
            self.conn.commit()
            return result
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

    def delete_data(self, table, columns=None):
        try:
            query = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
            # "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
            print("QUERY -> '{}'".format(query))
            self.cursor.execute(query)
            result = {}  # self.cursor.fetchall()  # FIND A WAY TO RETURN BACK THE DATA THAT'S JUST BEEN SAVED WITHIN THE DB
            self.conn.commit()
            return result
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

    def handle_ugcs_logic(self, obj, extra):  # HANDLE THE MAIN UGCS LOGIC RIGHT HERE ...
        try:
            """
            collection = self.validate_collection(extra)
            if collection is not None:
                obj = self.serialize_to("mongodb", obj)
                print("OBJECT {} -> {}".format(type(obj), obj))
                # NOW, YOU CAN SAVE THE DATA OBJECT
                self.db[collection].insert(obj, check_keys=False)
                # COZ YOU'RE LETTING MONGO-DB ALLOW '.' & '$' WITHIN YOUR KEYS, IT MIGHT HAVE SOME ISSUES
                # ISSUES WHEN YOU'RE USING A FILTER WITH .find({'key.prop':'value'}) TO ACCESS INNER DOCUMENTS
                return True
            return False
            """
            # 1ST, VALIDATE THAT THIS FILE'S DATA IS THE ACTUAL REQUIRED EXCEL FILE :)
            if (extra is not None) and ("table" in extra) and (extra["table"] == "Examination"):
                columns = ["EXAM_HALL", "COURSE_CODE", "PAPER_TITLE", "NO.", "INDEX_RANGE", "exam_time", "exam_date"]
                # for c in columns:  # DECIDE IF THIS VALIDATION CODE SNIPPET IS EVEN NECESSARY AT ALL
                #     if c not in obj.keys():  # DECIDE WHETHER THIS SHOULD RAISE AN ERROR TO STOP THE WHOLE FUNCTION
                #         raise Exception("COLUMN '{}' NOT AVAILABLE WITHIN THE DATA".format(c))

                # 1. RETRIEVE EXAM_HALL COLUMN
                #    NB: SOME OF THE VALUES HERE HAVE OPTIONS (eg. 'N' BLOCK / K. FOLSON BLDG.')
                #    BUT APPARENTLY, IT MIGHT NOT MATTER, COZ THAT'S THE SAME FORMAT WITHIN THE MYSQL DATABASE :)
                exam_hall = obj["EXAM_HALL"]

                # 2. ENTER 'venues' TABLE AND COMPARE 'EXAM_HALL' VALUE WITH ALL 'name' COLUMN VALUES
                #    GET THE 'id' OF THE FOUND ROW, OR CREATE A NEW ROW, AND THEN GET THE 'id' (AUTO-INCREMENTED)


                # 3. COMBINE id VALUE (AS 'venue_id') WITH obj DATA AND SAVE WITHIN THE 'schedules' TABLE
                #    'provisional' & 'semester' COLUMNS SHOULD ALWAYS HAVE THE VALUE 1
                #    CONCAT DATA OBJECT (USING THE MYSQLDB'S COLUMNS, NOT obj), IF IT'S NOT ALREADY WITHIN THE DATABASE, AND RETURN THE OBJ BACK
                #    OBJECT MUST BE RETURNED COZ YOU NEED TO KEEP TRACK OF THEM, IN CASE A REVERT/UNDO ACTION IS MADE


                # 4. PICK 'PAPER_TITLE' FROM obj & 'course_code' FROM 'schedules' ROW (OR 'COURSE_CODE' FROM obj, IF YOU WANT :)
                #    THEN ENTER 'courses' TABLE, AND INSERT A NEW ROW WITH DATA, IF IT DOESN'T ALREADY EXIST :)
                #    NB: 'PAPER_TITLE' -> 'title'; 'course_code' VALUE DETERMINES -> 'level' COLUMN; OTHER COLUMNS AUTO-GENERATED
                #


                # 5. RETURN SUCCESS RESULT, HOWEVER YOU SEE FIT :)


            else:
                print("SORRY, THERE IS NO table TO VALIDATE, OR THIS IS NOT THE 'Examination' TABLE :(")
        except Exception as e:
            print("ERROR -> {}".format(e))
        return None

