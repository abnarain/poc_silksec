import pytest
import sys
sys.path.append('../')
from  DBClient import MongoDBClient

@pytest.fixture
def setup():
    mongo_client = MongoDBClient("localhost",27017, "test_database", "test_collection")
    yield mongo_client
    mongo_client.close()

def test_db_works(setup):
    # Insert document
    mongo_client = setup
    document = {"name": "John", "age": 30}
    mongo_client.insert_document(document)

    # Find document
    query = {"name": "John"}
    result = mongo_client.find_document()
    print("Found document:", result)
    assert result["name"]  == "John"
    # Delete document
    mongo_client.delete_document(query)

def test_aggregate(setup):
    pass
    mongo_client = setup
    docs = [
    {"name": "John Doe", "age": 30},
     {"name": "John Doe", "age": 31},
     {"name": "John Doe", "age": 32},
     {"name": "John Doe", "age": 33},
     {"name": "John Doe", "age": 34},
     {"name": "John Doe", "age": 35}
     ]
    for doc in docs:
        mongo_client.insert_document(doc)
    x = [{"$group" : {"_id":"$name", "count":{"$sum":1}}}] 
    ans = mongo_client.agg_documents(x)
    ans = list(ans)
    ans = ans[0]
    assert ans['count'] == 6
    for doc in docs:
        mongo_client.delete_document(doc)

