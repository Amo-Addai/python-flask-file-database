import pandas as pd
import json
from database import Database
from file_system import FileSystem

DOWNLOAD_FOLDER = "/downloads/"


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
        def processFile(df, extra=None):
            print()
            print("NOW PROCESSING FILE -> {}".format(extra))
            if (extra is not None) and ("file_type" in extra) and ("filename" in extra):
                type, file = extra["file_type"], None
                if (len(extra["filename"]) > 0)(type in extra["filename"]):
                    filepath = "{}{}".format(DOWNLOAD_FOLDER, extra["filename"])
                    if type == "csv":
                        df.to_csv(filepath, sep=',')
                    elif type == "tsv":
                        df.to_csv(filepath, sep='\t')
                    elif (type == "xls") or (type == "xlsx"):
                        table = extra["table"] if (("table" in extra) and (len(extra["table"]) > 0)) else "Sheet1"
                        df.to_excel(filepath, sheet_name=table)
                    elif type == "json":
                        df.to_json(filepath)
                if file is not None:
                    print("RETURNING THE {} FILE".format(type))
                    return file
            return None

        try:
            print()
            print("PARAMS FOR RETRIEVING FILE -> {}".format(extra))
            df = None
            if ("source" in extra):
                if (extra["source"] == "db"):
                    data = self.database.get_data()  # PUT A table STRING AS A PARAM
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

    def preprocessData(self, df):  # DO SOME DATA PREPROCESSING, CLEANING, etc
        # FILL NAN VALUES; MAKE ALL DATETIME OBJECTS STRINGS OR STH;
        df = df.fillna("")
        return df, None

    def retrieve_data_from_file(self, df, extra):  # RETRIEVE THE DATA FROM df & SAVE WITHIN THE DB
        table = "GET THE TABLE NAME NOWWW!!"  # MAKE SURE YOU FIND TABLE NAMES FOR THE DATABASE
        #   HOWEVER, FOR NOW, A DEFAULT TABLE (Examination) IS BEING USED
        if (df is not None) and (len(df) > 0):
            df, err = self.preprocessData(df)
            if err is None:
                for index, row in df.iterrows():
                    try:
                        print("NOW, SAVING OBJECT OF INDEX -> {}".format(index))
                        self.database.save_data_object(row.to_dict())
                    except Exception as e:
                        print("ERROR IN SAVING OBJECT -> {}".format(e))
                # NOW, JUST TEST HOW TO RETRIEVE DATA BACK FROM THE DATABASE
                extra["source"] = "db"
                self.retrieve_file_from_database_or_file_system(extra)
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
                elif type == "tsv":
                    df.read_csv(file, sep='\t')
                elif (type == "xls") or (type == "xlsx"):
                    df = pd.read_excel(file)
            if df is not None:
                print(df.head())
                if self.retrieve_data_from_file(df, extra):
                    #   DECIDE WHETHER TO SAVE THIS FILE IN THE UPLOAD FOLDER OR NOT 1ST!!!
                    if ("save_to_file_system" in extra) and (extra["save_to_file_system"]):
                        print("Saving file to the file system too")
                        self.file_system.save_file(file, extra)
                    return True
        except Exception as e:
            print("SOME ERROR OCCURRED (handle_file()) -> {}".format(e))
        print("COULDN'T RETRIEVE DATA FROM THE FILE")
        return False
