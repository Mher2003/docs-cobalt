import jwt
import datetime
from hashlib import sha256
from flask import current_app

def token_login(password):
    """
    Check password and generate a JWT with an expiration of 30 minutes
    :param password: Server password
    >>> token_login("password1234")
    """
    if(sha256(password.encode("utf-8")).hexdigest() == current_app.config["PASSWORD_HASHED"]):
        token = jwt.encode({'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)}, current_app.config["JWT_SECRET"], algorithm="HS256")
        return token
    return False

def token_check(token):
    """
    Validate a JWT
    :param token: JWT token
    >>> token_check("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.sr08LEMNntsBjm8vu8Xv1ciDBmKZUv-dRKiO2efI7KI")
    """
    try:
        jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
    except:
        return False
    return True
