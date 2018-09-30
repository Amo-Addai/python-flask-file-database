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


class Database:
    db = None
    default_table = "Examination"

    def __init__(self):
        pass

    def setup_db(self, app):
        name = DATABASE['name']
        app.config["MONGO_URI"] = MONGO_URI
        mongoclient = pymongo.MongoClient(MONGO_URI)
        dblist = mongoclient.list_database_names()
        print("DATABASES -> {}".format(dblist))
        self.db = mongoclient[name]
        for table in DATABASE["tables"]:
            print("Creating Database Table {} -> {}".format(table, self.db[table]))
            print("Now, Clearing Database Table {} -> {} items".format(self.db[table].remove(),
                                                                       self.db[table].find().count()))
        return app

    def get_data(self, filter=None, table=default_table):
        data = self.db[table].find(filter if (filter is not None) else {})
        #   NOW, WORK WITH data HOWEVER YOU WANT
        for obj in data:  # MAKE SURE YOU UNHASH ALL THE PINS FIRST THOUGH
            if 'pin' in obj:
                obj['pin'] = self.unhash_pin(obj['pin'])

        return data

    def save_data_object(self, obj, table=default_table):
        print("OBJECT {} -> {}".format(type(obj), obj))
        # 1ST, TRY TO DO SOME FURTHER PREPROCESSING (eg. CONVERT datetime.time OBJECTS INTO STRINGS)
        if 'pin' in obj:
            print("NOW, HASHING PIN -> {}".format(obj['pin']))
            obj['pin'] = self.hash_pin(obj['pin'])
        # NOW, YOU CAN SAVE THE DATA OBJECT
        self.db[table].save(obj, check_keys=False)
        # COZ YOU'RE LETTING MONGO-DB ALLOW '.' & '$' WITHIN YOUR KEYS, IT MIGHT HAVE SOME ISSUES
        # ISSUES WHEN YOU'RE USING A FILTER WITH .find({'key.prop':'value'}) TO ACCESS INNER DOCUMENTS

    def hash_pin(self, pin):  # FIND OUT THE KEY YOU'RE USING TO HASH THE PINS
        h = hashlib.md5(pin.encode())
        hashedString = h.hexdigest()
        print("HASH -> {}".format(hashedString))
        return hashedString

    def unhash_pin(self, pin):
        pass
