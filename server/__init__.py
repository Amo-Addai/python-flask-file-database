import pandas as pd
import json, os
from database import Database
from database.mysql_db import MySQLDatabase
from file_system import FileSystem

DATABASE_MODE = "MYSQL"
# os.path.join(current_directory, "/server/downloads/") OR os.getcwd()
current_directory = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_FOLDER = current_directory + "/downloads/"
print(DOWNLOAD_FOLDER)  # 'C:\Users\kwadw\Desktop\file-database\server/downloads/


class Server:
    database, file_system = None, None

    def __init__(self):
        pass

    def setup_db_and_file_system(self, app):  # SETUP THE DATABASE AND FILE SYSTEM ENVIRONMENTS
        self.database = Database()
        self.mysql_database = MySQLDatabase()
        self.file_system = FileSystem()
        app = self.database.setup_db(app)
        app = self.mysql_database.setup_mysql_db(app)
        app = self.file_system.setup_file_system(app)
        return app

    def get_collections(self, query):
        category = "All"
        if ("category" in query) and (len(query["category"]) > 0):
            category = query["category"]
        data = self.database.get_collections(category)
        print("DATA -> {}".format(data))
        json_data = json.loads(json.dumps(data))
        print("JSON DATA -> {}".format(json_data))
        return json_data

    def delete_collection(self, extra):
        try:
            print("ABOUT TO DELETE COLLECTION WITH PARAMS -> {}".format(extra))
            return self.database.delete_collection(extra)
        except Exception as e:
            print("ERROR WHILE DELETING COLLECTION -> {}".format(e))
        return False

    def retrieve_file_from_database_or_file_system(self, filter, extra):  # RETRIEVE THE DATA FROM DB & PREPARE FILE
        def processFile(df, extra=None):
            def to_xml(df, filename=None, mode='w'):
                def row_to_xml(row):
                    xml = ['<item>']
                    for i, col_name in enumerate(row.index):
                        xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
                    xml.append('</item>')
                    return '\n'.join(xml)

                res = "{}\n{}\n{}".format('<xml>', ('\n'.join(df.apply(row_to_xml, axis=1))), '</xml>')
                if filename is None:
                    return res
                with open(filename, mode) as f:
                    f.write(res)

            try:
                print()
                print("NOW PROCESSING FILE -> {}".format(extra))
                if (extra is not None) and ("file_type" in extra) and ("filename" in extra):
                    type, file, filepath, filename = extra["file_type"], None, None, None
                    if (len(extra["filename"]) > 0) and (len(type) > 0):
                        filename = "{}.{}".format(extra["filename"], type)
                        filepath = "{}{}".format(DOWNLOAD_FOLDER, filename)
                        print("PATH -> '{}'".format(filepath))
                        if type == "csv":
                            df.to_csv(filepath, sep=',')
                        elif type == "tsv":
                            df.to_csv(filepath, sep='\t')
                        elif (type == "xls") or (type == "xlsx"):
                            sheet_name = extra["collection"] if (
                                ("collection" in extra) and (len(extra["collection"]) > 0)) else "Sheet1"
                            print("EXCEL SHEET '{}'".format(sheet_name))
                            df.to_excel(filepath, sheet_name=sheet_name)
                        elif type == "html":
                            df.to_html(filepath)
                        elif type == "xml":  # ASSIGNING CUSTOM to_xml() FUNCTION
                            pd.DataFrame.to_xml = to_xml
                            df.to_xml(filepath)  # WHEN RETURNED TO CLIENT, RESPONSE IS IN .error() CALLBACK :(
                        elif type == "sql":
                            df.to_sql(filepath)
                        elif type == "json":
                            print("JSON STRING -> {}".format(df.to_json()))
                            df.to_json(filepath, orient='index')  # CANNOT CONVERT TO .json FILE WITHOUT PROPERLY :(
                        elif type == "txt":
                            raise Exception
                        elif type == "pdf":
                            raise Exception
                        print("RETURNING THE .{} FILE-PATH -> {}".format(type, filepath))
                        return filepath, filename
            except Exception as e:
                print("ERROR DURING PROCESSING OF FILE -> {}".format(e))
            return None, None

        try:
            print("PARAMS FOR RETRIEVING FILE -> {}".format(extra))
            df = None
            if ("source" in extra):
                data = None
                if (extra["source"] == "db"):
                    if DATABASE_MODE == "MONGODB":
                        data = self.database.get_data(filter, extra)
                    elif DATABASE_MODE == "MYSQL":  # PUT IN PROPER PARAMS FOR THIS MYSQL-DB METHOD :)
                        data = self.mysql_database.get_data(filter, extra)
                    else:
                        raise Exception("INCORRECT DATABASE MODE SELECTED -> '{}'".format(DATABASE_MODE))
                    if data is not None:
                        df = pd.DataFrame(data)
                elif (extra["source"] == "fs"):
                    if "filename" in extra:
                        filename = extra["filename"]
            if df is not None:
                print("DATAFRAME IS READY ({} items)".format(len(df)))
                print(df.head())
                # NOW, PROCESS THIS data INTO A DATAFRAME, THEN INTO ANY FILETYPE (eg. xlsx, etd)
                return processFile(df, extra)
            else:
                print("DATAFRAME COULD NOT BE RETRIEVED SUCCESSFULLY")
        except Exception as e:
            print("ERROR IN RETRIEVING FILE -> {}".format(e))
        return False

    def retrieve_data_from_file(self, df, extra):  # RETRIEVE THE DATA FROM df & SAVE WITHIN THE DB
        def preprocessData(df):  # DO SOME DATA PREPROCESSING, CLEANING, etc
            # FILL NAN VALUES; MAKE ALL DATETIME OBJECTS STRINGS OR STH;
            df = df.fillna("")
            return df, None

        #   HOWEVER, FOR NOW, A DEFAULT COLLECTION (Examination) IS BEING USED
        if (df is not None) and (len(df) > 0):
            df, err = preprocessData(df)
            if err is None:
                success = None
                for index, row in df.iterrows():
                    try:
                        print()
                        print("NOW, SAVING OBJECT OF INDEX -> {}".format(index))
                        if DATABASE_MODE == "MONGODB":
                            success = self.database.save_data_object(row.to_dict(), extra)
                        elif DATABASE_MODE == "MYSQL":
                            SHOULD_HANDLE_UGCS_LOGIC = True
                            if SHOULD_HANDLE_UGCS_LOGIC:
                                success = self.mysql_database.handle_ugcs_logic(row.to_dict(), extra)
                        else:
                            raise Exception("INCORRECT DATABASE MODE SELECTED -> '{}'".format(DATABASE_MODE))
                        # WORK WITH success HOWEVER YOU WANT ..
                        print()
                    except Exception as e:
                        print("ERROR IN SAVING OBJECT -> {}".format(e))
                print()
                return True
            else:
                print("Error during preprocessing of the Data")
        else:
            print("Dataset is either empty or unavailable")
        return False

    def handle_file(self, file, extra):
        def save_to_file_system(fs):
            #   DECIDE WHETHER TO SAVE THIS FILE IN THE UPLOAD FOLDER OR NOT 1ST!!!
            if ("save_to_file_system" in extra) and (extra["save_to_file_system"]):
                print("Saving file to the file system too")
                fs.save_file(file, extra)

        df = None
        try:
            if 'file_type' in extra:
                type = extra['file_type']
                if type == "csv":
                    df = pd.read_csv(file)
                elif type == "tsv":
                    df.read_csv(file, sep='\t')
                elif (type == "xls") or (type == "xlsx"):
                    print("a")
                    df = pd.read_excel(file)
            if df is not None:
                print(df.head())
                if self.retrieve_data_from_file(df, extra):
                    save_to_file_system(self.file_system)
                    return True
                else:  # YOU CAN ALSO SAVE THE FILE WITHIN THE FILE-SYSTEM, IN CASE DATA CANNOT BE RETRIEVED ..
                    pass
        except Exception as e:
            print("SOME ERROR OCCURRED (handle_file()) -> {}".format(e))
            save_to_file_system(self.file_system)  # IN CASE OF ANY ERRORS, YOU CAN ALSO SAVE FILE TO THE FILE SYSTEM :)
        print("COULDN'T RETRIEVE DATA FROM THE FILE")
        return False

    def request_file(self, filter, extra):
        def preprocessFilter(filter):
            if filter is not "all":
                pass  # NOW, YOU CAN DO YOUR FILTER PREPROCESSING (eg. VALIDATION, etc) RIGHT HERE ..
            if "source" not in extra:
                extra["source"] = "db"
            return filter

        try:
            filter = preprocessFilter(filter)
            return self.retrieve_file_from_database_or_file_system(filter, extra)
        except Exception as e:
            print("SOME ERROR OCCURRED (request_file()) -> {}".format(e))
        print("COULDN'T RETRIEVE FILE FROM THE FILE-DATABASE")
        return None
