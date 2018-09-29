import pymongo, hashlib

"""
START MONGO DAEMON INSTANCE - "C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe"
START MONGO CLI APP - "C:\Program Files\MongoDB\Server\3.4\bin\mongo.exe"
"""
MONGO_URI = "mongodb://localhost:27017/"
DATABASE = {
    'name': "ugcs",
    'tables': ["Examination"]
}
mongodb = None
db = None


def setup_db(app):
    name = DATABASE['name']
    app.config["MONGO_URI"] = MONGO_URI
    mongoclient = pymongo.MongoClient(MONGO_URI)
    dblist = mongoclient.list_database_names()
    print("DATABASES -> {}".format(dblist))
    mongodb = mongoclient[name]
    db = mongodb[name]
    for table in DATABASE["tables"]:
        print("CREATING DB TABLE -> {}".format(table))
        db.createCollection(table)
    return app


def get_data(table):
    data = db[table].find()
    #   NOW, WORK WITH data HOWEVER YOU WANT
    for obj in data:  # MAKE SURE YOU UNHASH ALL THE PINS FIRST THOUGH
        if 'pin' in obj:
            obj['pin'] = unhash_pin(obj['pin'])

    return data


def save_data_object(table, obj):
    print("OBJECT -> {}".format(obj))  # NOW, YOU CAN SAVE THE DATA OBJECT
    if 'pin' in obj:
        print("NOW, HASHING PIN -> {}".format(obj['pin']))
        obj['pin'] = hash_pin(obj['pin'])
        print("HASH -> {}".format(hash))
    db[table].save(obj)


def hash_pin(pin):  # FIND OUT THE KEY YOU'RE USING TO HASH THE PINS
    h = hashlib.md5(pin.encode())
    hash = h.hexdigest()
    return hash


def unhash_pin(pin):
    pass
