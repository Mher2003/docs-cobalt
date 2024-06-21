import jwt
import datetime
from hashlib import sha256

JWT_SECRET = "SECRET"

def token_login(password):
    if(sha256(password.encode("utf-8")).hexdigest() == "b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3"):
        token = jwt.encode({'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)}, JWT_SECRET, algorithm="HS256")
        return token
    return False

def token_check(token):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except:
        return False
    return True
