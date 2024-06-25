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
    return "Cobalt Docs V Beta 1.5"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.form["token"]
        except:
            try:
                data = request.get_json()
                token = data["token"]
                print(data["token"])
            except:
                return response_error_no_token()
        if not token:
            return response_error_no_token()
        if(not token_check(token)):
            return response_error_invalid_token()
        return f(*args, **kwargs)
    return decorated

@server.route('/token', methods=['POST'])
def login():

    try:
        request_data = request.get_json()
    except:
        return response_error_not_supported()
    try:
        password = request_data["password"]
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
        request_data = request.get_json()
    except:
        return response_error_not_supported()
    
    try:
        type = request_data["type"]
    except:
        return response_error_no_file()

    try:
        filename = request_data["filename"]
    except:
        return response_error_no_file()
    
    id = addFile(type, filename)

    if(not id):
        return response_error_filename_exists()
    
    CreateQR(baseURL, docsdir, id, type, filename)

    return response_document(id)

@server.route('/file', methods = ['POST'])
@token_required
def file_upload():
    try:
        id = request.form["document_id"]
    except:
        return response_error_no_document_id()

    try:
        f = request.files["file"]
    except:
        return response_error_no_file()
    
    record = findID(id)

    if(not record):
        return response_error_invalid_document_id()
    
    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    
    return response_document(id)

