from hashlib import sha256
from uuid import uuid4

sessions= []

def login(password):
    if(checkPassword(password)):
        sessionID = str(uuid4())
        sessions.append(sessionID)
        return sessionID
    return False

def deleteSession(sessionID):
    if (sessionID in sessions):
        sessions.remove(sessionID)
        return True
    return False

def checkSession(sessionID):
    if (sessionID in sessions):
        return True
    return False

def checkPassword(password):
    if(sha256(password.encode('utf-8')).hexdigest() == "b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3"):
        return True
    return False