from pymongo import MongoClient
from flask import current_app
import datetime as dt
import uuid

def mongodb_connect(mongodb_address):
    cluster = MongoClient(mongodb_address)
    database = cluster["docs"]
    global db_docs
    db_docs = database["docs"]
    return True

def document_find_by_id(id):
    result = db_docs.find_one({"_id":id})
    if result:
        return result
    return False

def findFile(directory,filename):
    result = db_docs.find_one({"directory":directory,"filename":filename})
    if result:
        return result
    return False

def document_find_last_n(n):
    if(n <= 0):
        return False
    results = list(db_docs.find().sort({"time": -1}).limit(n))
    return results


def document_create_record(directory,filename):
    if(not findFile(directory, filename)) and isinstance(filename, str):
        id = str(uuid.uuid4())
        now = dt.datetime.utcnow().timestamp()
        record = {
            "_id":id,
            "host":"https://docs.cobalt.am/",
            "directory":directory,
            "filename":filename,
            "time":now
        }
        db_docs.insert_one(record)
        return id
    return False

def document_change_time(id):
    now = dt.datetime.utcnow().timestamp()
    record = db_docs.update_one({"_id":id}, {"$set":{"time": now}})
    if(record):
        return True
    return False


def delete_record(id):
    record = document_find_by_id(id)
    if(record):
        return True
    return False