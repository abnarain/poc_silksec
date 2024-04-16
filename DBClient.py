import pymongo

class MySQLDBClient:
    pass


class SomeOtherDBClient:
    pass


class MongoDBClient:
    def __init__(self, uri, port, db_name, collection_name):
        self.client = pymongo.MongoClient(uri, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_document(self, document):
        self.collection.insert_one(document)

    def find_document(self, query):
        return self.collection.find_one(query)
    
    def find_documents(self, query=None):
        return self.collection.find(query)

    def find_documents(self):
        return self.collection.find()

    def agg_documents(self, query):
        return self.collection.aggregate(query)



    def update_document(self, query, new_values):
        self.collection.update_one(query, {"$set": new_values})
        print("Document updated successfully.")

    def delete_document(self, query):
        self.collection.delete_one(query)
        print("Document deleted successfully.")

    def close(self):
        self.client.close()

