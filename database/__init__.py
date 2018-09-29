import pymongo, hashlib

"""
START MONGO DAEMON INSTANCE - "C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe"
START MONGO CLI APP - "C:\Program Files\MongoDB\Server\3.4\bin\mongo.exe"
"""
MONGO_URI = "mongodb://localhost:27017/"
DATABASE = {
    'name': "ugcs"
}
mongodb = None
db = None


def setup_db(app):
    name = DATABASE['name']
    app.config["MONGO_URI"] = MONGO_URI
    mongodb = pymongo.MongoClient(MONGO_URI)[name]
    dblist = mongodb.list_database_names()
    print("DATABASES -> {}".format(dblist))
    if name in dblist:
        print("DATABASE EXISTS -> {}".format(name))
        db = mongodb[name]
    return app


def get_data(table):
    data = db[table].find()
    #   NOW, WORK WITH data HOWEVER YOU WANT
    for obj in data:  # MAKE SURE YOU UNHASH ALL THE PINS FIRST THOUGH
        if 'pin' in obj:
            obj['pin'] = unhash_pin(obj['pin'])

    return data


def save_data_object(table, obj):
    obj = {}
    for key in ['a']:
        obj[key] = obj[key] if key in obj else ""
    print("OBJECT -> {}".format(obj))  # NOW, YOU CAN SAVE THE DATA OBJECT
    if 'pin' in obj:
        obj['pin'] = hash_pin(obj['pin'])
    db[table].save(obj)


def hash_pin(pin):  # FIND OUT THE KEY YOU'RE USING TO HASH THE PINS
    h = hashlib.md5(pin.encode())
    hash = h.hexdigest()
    print("HASH -> {}".format(hash))
    return hash


def unhash_pin(pin):
    pass
