import pandas as pd
import database, file_system


def setup_db_and_file_system(app):  # SETUP THE DATABASE AND FILE SYSTEM ENVIRONMENTS
    app = database.setup_db(app)
    return file_system.setup_file_system(app)


def retrieve_file_from_database_or_file_system(extra):  # RETRIEVE THE DATA FROM DB & PREPARE FILE
    data = database.get_data()  # PUT A table STRING AS A PARAM
    pass


def retrieve_data_from_file(df):  # RETRIEVE THE DATA FROM df & SAVE WITHIN THE DB
    table = "GET THE TABLE NAME NOWWW!!"
    if (df is not None) and (df.size > 0):
        for index, row in df.iterrows():
            print("NOW, SAVING OBJECT OF INDEX -> {}".format(index))
            database.save_data_object(table, row)
        return True
    else:
        print("Dataset is either empty or unavailable")
    return False


def handle_file(file, extra):
    df = None
    if 'file_type' in extra:
        type = extra['file_type']
        if type is "csv":
            df = pd.read_csv(file)
        elif (type is "xls") or (type is "xlsx"):
            df = pd.read_excel(file)
    if df is not None:
        if retrieve_data_from_file(df):
            #   DECIDE WHETHER TO SAVE THIS FILE IN THE UPLOAD FOLDER OR NOT 1ST!!!
            if ("save_to_file_system" in extra) and (extra["save_to_file_system"]):
                print("Saving file to the file system too")
                file_system.save_file(file, extra)
            return True
    print("COULDN'T RETRIEVE DATA FROM THE FILE")
    return False
