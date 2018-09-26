import pandas as pd
import hashlib

from flask_pymongo import PyMongo


mongo = None

def setup_db(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    mongo = PyMongo(app)
    return app


def get_data(table):
    data = mongo.db[table].find()
    #   NOW, WORK WITH data HOWEVER YOU WANT
    return data


def hash_pin(pin):
    h = hashlib.md5(pin.encode())
    hash = h.hexdigest()
    print("HASH -> {}".format(hash))
    return hash


def save_data_object(table, row):
    obj = {}
    for key in ['a']:
        obj[key] = row[key] if key in row else ""
    print("OBJECT -> {}".format(obj))  # NOW, YOU CAN SAVE THE DATA OBJECT
    obj['pin'] = hash_pin(obj['pin'])
    mongo.db[table].save(row)


def retrieve_data_from_file(df):  # RETRIEVE THE DATA FROM df & SAVE WITHIN THE DB
    df = pd.DataFrame()
    if (df is not None) and (df.size > 0):
        for index, row in df.iterrows():
            print("NOW, SAVING OBJECT OF INDEX -> {}".format(index))
            save_data_object(row)
    else:
        print("DATASET IS EMPTY")
        return True
    return False


def handle_file(file, extra):
    df = None
    if extra['type'] is "csv":
        df = pd.read_csv(file)
    elif extra['type'] is "xls":
        df = pd.read_excel(file)

    if df is not None:
        if retrieve_data_from_file(df):
            return True
    print("COULDN'T RETRIEVE DATA FROM THE FILE")
    return False
