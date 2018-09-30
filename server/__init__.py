import pandas as pd
import json
from database import Database
from file_system import FileSystem


class Server:
    database, file_system = None, None

    def __init__(self):
        pass

    def setup_db_and_file_system(self, app):  # SETUP THE DATABASE AND FILE SYSTEM ENVIRONMENTS
        self.database = Database()
        self.file_system = FileSystem()
        app = self.database.setup_db(app)
        return self.file_system.setup_file_system(app)

    def retrieve_file_from_database_or_file_system(self, extra):  # RETRIEVE THE DATA FROM DB & PREPARE FILE
        data = self.database.get_data()  # PUT A table STRING AS A PARAM
        pass

    def preprocessData(self, df):  # DO SOME DATA PREPROCESSING, CLEANING, etc
        # FILL NAN VALUES; MAKE ALL DATETIME OBJECTS STRINGS OR STH;
        df = df.fillna("")
        return df, None

    def retrieve_data_from_file(self, df):  # RETRIEVE THE DATA FROM df & SAVE WITHIN THE DB
        table = "GET THE TABLE NAME NOWWW!!"  # MAKE SURE YOU FIND TABLE NAMES FOR THE DATABASE
        #   HOWEVER, FOR NOW, A DEFAULT TABLE (Examination) IS BEING USED
        if (df is not None) and (df.size > 0):
            df, err = self.preprocessData(df)
            if err is None:
                for index, row in df.iterrows():
                    try:
                        print("NOW, SAVING OBJECT OF INDEX -> {}".format(index))
                        # BUT 1ST, MAKE SURE THIS IS A JSON OBJECT, AND NOT A PANDAS SERIES OBJECT
                        obj = json.loads(json.dumps(str(row.to_dict())))
                        self.database.save_data_object(obj)
                    except Exception as e:
                        print("ERROR IN SAVING OBJECT -> {}".format(e))
                return True
            else:
                print("Error during preprocessing of the Data")
        else:
            print("Dataset is either empty or unavailable")
        return False

    def handle_file(self, file, extra):
        df = None
        try:
            if 'file_type' in extra:
                type = extra['file_type']
                if type == "csv":
                    df = pd.read_csv(file)
                elif (type == "xls") or (type == "xlsx"):
                    df = pd.read_excel(file)
            if df is not None:
                print(df.head())
                if self.retrieve_data_from_file(df):
                    #   DECIDE WHETHER TO SAVE THIS FILE IN THE UPLOAD FOLDER OR NOT 1ST!!!
                    if ("save_to_file_system" in extra) and (extra["save_to_file_system"]):
                        print("Saving file to the file system too")
                        self.file_system.save_file(file, extra)
                    return True
        except Exception as e:
            print("SOME ERROR OCCURRED (handle_file()) -> {}".format(e))
        print("COULDN'T RETRIEVE DATA FROM THE FILE")
        return False
