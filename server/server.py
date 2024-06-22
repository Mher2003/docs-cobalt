from flask import Blueprint, request
from flask_cors import cross_origin
from functools import wraps
import os, datetime
from .auth import token_login, token_check
from .db import findID, addFile, change_time
from .qr import CreateQR
from .response import *

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
    return "Cobalt Docs V1.4"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.form["token"]
        except:
            return response_error_no_token()
        if not token:
            return 
        if(not token_check(token)):
            return response_error_invalid_token()
        return f(*args, **kwargs)
    return decorated

@server.route('/token', methods=['POST'])
def login():
    try:
        password = request.form["password"]
    except:
        return response_error_no_password()
    token = token_login(password) 
    if(not token):
        return response_error_wrong_password()
    return response_token(token)

@server.route('/document', methods = ['POST'])
@token_required
def document_add():
   
    try:
        f = request.files["file"]
    except:
        return response_error_no_file()
    
    try:
        filename = request.form["filename"]
    except:
        return response_error_no_file()
    
    try:
        type = request.form["type"]
    except:
        return response_error_no_file()
    
    id = addFile(type, filename)

    if(not id):
        return response_error_filename_exists()
    
    record = findID(id)
    qr = CreateQR(baseURL, docsdir, id, type, filename)

    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    
    return response_document(id)

@server.route('/document', methods = ['PATCH'])
@token_required
def document_edit():
    f,id = request.files["file"],request.form["id"]
    record = findID(id)
    if((not record) or (not f)):
        return response_error_no_file()
    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    return "True"

