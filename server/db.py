from pymongo import MongoClient
import datetime as dt
import uuid
from .types import isType

def connect():
    cluster = MongoClient("mongodb://localhost:27017")
    database = cluster["docs"]
    global db_docs
    db_docs = database["docs"]
    return True

def findID(id):
    result = db_docs.find_one({"_id":id})
    if result:
        return result
    return False

def findFile(type,file):
    result = db_docs.find_one({"type":type,"file":file})
    if result:
        return result
    return False

def findLastNFiles(n):
    if(n <= 0):
        return False
    results = list(db_docs.find().sort({'create': -1}).limit(n))
    return results


def addFile(type,file):
    if(not findFile(type, file)) and isType(type) and isinstance(file, str):
        id = str(uuid.uuid4())
        now = dt.datetime.utcnow().timestamp()
        record = {
            "_id":id,
            "type":type,
            "file":file,
            "create":now,
            "update":float(0)
        }
        db_docs.insert_one(record)
        return id
    return False

def change_time(id):
    now = dt.datetime.utcnow().timestamp()
    record = db_docs.update_one({"_id":id}, {"$set":{"update": now}})
    if(record):
        return True
    return False


def delete_record(id):
    record = findID(id)
    if(record):
        return True
    return False