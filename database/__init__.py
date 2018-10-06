import pymongo, datetime

# from Crypto.Cipher import AES

"""
START MONGO DAEMON INSTANCE - "C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe"
START MONGO CLI APP - "C:\Program Files\MongoDB\Server\3.4\bin\mongo.exe"
"""
MONGO_URI = "mongodb://localhost:27017/"
DATABASE = {
    'name': "ugcs",
    'collections': ["Examination"]
}


class Database:
    db, encryption = None, None
    default_collection = "Examination"

    def __init__(self):
        self.encryption = self.Encryption()

    def setup_db(self, app):
        name = DATABASE['name']
        app.config["MONGO_URI"] = MONGO_URI
        mongoclient = pymongo.MongoClient(MONGO_URI)
        dblist = mongoclient.list_database_names()
        print("DATABASES -> {}".format(dblist))
        self.db = mongoclient[name]
        for collection in DATABASE["collections"]:
            print("Creating Database Collection '{}' -> {}".format(collection, self.db[collection]))
            print("Now, Clearing Database Collection '{}' -> {} item(s)".format(self.db[collection].remove(),
                                                                           self.db[collection].find().count()))
            self.test_db(collection)
        return app

    def test_db(self, collection=default_collection):
        #   FIRST, TEST THE DATABASE CRUD OPERATIONS
        obj1, obj2, obj3 = {"hello": "world1"}, {"hello": "world2"}, {"hello": "world3"}
        # obj["hello"] = self.encryption.encrypt(obj["hello"])
        print(self.db[collection].insert([obj1, obj2, obj3]))
        print(self.db[collection].find().count())
        print("DONE SAVING DATA, NOW GETTING IT ALL BACK")
        cursor, data = self.db[collection].find(), []
        for o in cursor:
            print()
            print(o)
            # if "hello" in o:
            #     print("NOW, DECRYPTING DATA")
            #     o["hello"] = self.encryption.decrypt(o["hello"])
            #     print(o)
            data.append(o)
        print()
        print("DONE DECRYTING ALL DATA")
        print("{} item(s) -> {}".format(len(data), data))
        print("Done testing, Clearing Database Collection '{}' again -> {} item(s)".format(self.db[collection].remove(),
                                                                                      self.db[collection].find().count()))
        print()

    def get_data(self, filter=None, collection=default_collection):
        cursor, data = self.db[collection].find(filter if (filter is not None) else {}), []
        for o in cursor:
            print()
            print(o)
            o = self.serialize_to("dict", o)
            data.append(o)
        print()
        print("DONE RETRIEVING AND DECRYPTING ALL DATA")
        print("{} item(s) -> {}".format(len(data), data))
        return data

    def save_data_object(self, obj, collection=default_collection):
        obj = self.serialize_to("mongodb", obj)
        print("OBJECT {} -> {}".format(type(obj), obj))
        # NOW, YOU CAN SAVE THE DATA OBJECT
        self.db[collection].insert(obj, check_keys=False)
        # COZ YOU'RE LETTING MONGO-DB ALLOW '.' & '$' WITHIN YOUR KEYS, IT MIGHT HAVE SOME ISSUES
        # ISSUES WHEN YOU'RE USING A FILTER WITH .find({'key.prop':'value'}) TO ACCESS INNER DOCUMENTS

    def serialize_to(self, param, obj):
        if param == "mongodb":  # 1ST, TRY TO DO SOME FURTHER PREPROCESSING (eg. CONVERT datetime.time OBJECTS INTO STRINGS)
            print("Serializing from Dictionary to Mongo-DB object")
            if 'pin' in obj:
                print("NOW, ENCRYPTING PIN -> {}".format(obj['pin']))
                obj['pin'] = self.encryption.encrypt(obj['pin'])
            for key in obj:
                if type(obj[key]) is datetime.time:
                    obj[key] = obj[key].strftime("%H:%M:%S")
        elif param == "dict":
            print("Serializing from Mongo-DB to Dictionary object")
            if 'pin' in obj:
                print("NOW, DECYPTING PIN -> {}".format(obj['pin']))
                obj['pin'] = self.encryption.decrypt(obj['pin'])
            for key in obj:
                pass
                # FIND A WAY TO CONVERT "TIME STRING" BACK TO A datetime.time OBJECT
                # if type(obj[key]) is datetime.time:
                #     obj[key] = obj[key].strftime("%H:%M:%S")
        else:
            print("Incorrect parameter value")
        print("SERIALIZED OBJECT -> {}".format(obj))
        return obj

    class Encryption:
        key, nonce = "", None

        def __init__(self, key="DEFAULT KEY COMES HERE"):
            self.key = key
            self.nonce = None

        def encrypt(self, text):  # FIND OUT THE KEY YOU'RE USING TO ENCRYPT THE PINS
            # self.cipher = AES.new(self.key, AES.MODE_EAX)
            # self.nonce = self.cipher.nonce
            # ciphertext, self.tag = self.cipher.encrypt_and_digest(text)
            # return ciphertext
            pass

        def decrypt(self, ciphertext):
            # try:
            #     self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
            #     plaintext = self.cipher.decrypt(ciphertext)
            #     self.cipher.verify(self.tag)
            #     print("The message is authentic:", plaintext)
            #     return plaintext
            # except ValueError:
            #     print("Key incorrect or message corrupted")
            #     print("Returning Ciphertext back")
            # return ciphertext
            pass
