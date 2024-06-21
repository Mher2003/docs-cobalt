from flask import Blueprint, jsonify, request, make_response
from functools import wraps
import os, datetime
from .auth import token_login, token_check
from .db import findID, addFile, change_time
from .qr import CreateQR

server = Blueprint('register', __name__)

def setDocsDir(dir):
    global docsdir
    docsdir = dir

def setTypes(type):
    global types
    types=type

def setBaseURL(url):
    global baseURL
    baseURL = url

@server.route('/', methods= ['GET'])
def home():
    return "Cobalt Docs V1.2"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return "No Token"

        if(not token_check(token)):
            return "Wrong Token"
        return f(*args, **kwargs)
    return decorated

@server.route('/login', methods=['POST'])
def log():
    try:
        password = request.form["password"]
    except:
        return "No Password supplied"

    token = token_login(password) 
    if(not token):
        return "Wrong Password"
    response = make_response()
    response.set_cookie("token", token)
    return response

@server.route('/document', methods = ['POST'])
@token_required
def document_add():
    f = request.files["file"]
    id = addFile(request.form["type"],request.form["filename"])
    
    if(not id):
        return "Filename exists"
    
    record = findID(id)
    qr = CreateQR(baseURL, docsdir, id, request.form["type"], request.form["filename"])

    if(not f):
        return "File doesn't exists"
    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    
    return id

@server.route('/document', methods = ['PATCH'])
@token_required
def document_edit():
    f,id = request.files["file"],request.form["id"]
    record = findID(id)
    if((not record) or (not f)):
        return "File doesn't exists"
    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    return "True"

