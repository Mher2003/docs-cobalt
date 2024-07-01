import urllib
import os
from flask import Blueprint, request, current_app
from functools import wraps
from .auth import *
from .db import *
from .qr import *
from .response import *

server = Blueprint("register", __name__)

@server.route("/", methods= ["GET"])
def home():
    return "Cobalt Docs V Beta 1.6"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.form["token"]
        except:
            try:
                data = request.get_json()
                token = data["token"]
            except:
                return response_error_no_token()
        if not token:
            return response_error_no_token()
        if(not token_check(token)):
            return response_error_invalid_token()
        return f(*args, **kwargs)
    return decorated

@server.route("/token", methods=["POST"])
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

@server.route("/documents", methods = ["GET"])
def documents_get():
    data = document_find_last_n(5)

    results = []

    for record in data:
        results.append({
            "Filename": record["filename"],
            "URL": urllib.parse.urljoin(current_app.config["BASE_URL"],record["directory"]+"/"+record["filename"]),
            "Time": record["create"]
    })
        
    return response_documents(results)

@server.route("/document", methods = ["POST"])
@token_required
def document_add():
    try:
        request_data = request.get_json()
    except:
        return response_error_not_supported()
    
    try:
        directory = request_data["directory"]
    except:
        return response_error_no_file()

    try:
        filename = request_data["filename"]
    except:
        return response_error_no_file()
    
    id = document_create_record(directory, filename)

    if(not id):
        return response_error_filename_exists()
    
    return response_document(id)

@server.route("/file", methods = ["POST"])
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
    
    record = document_find_by_id(id)

    if(not record):
        return response_error_invalid_document_id()
    
    file = os.path.join(current_app.config["DOCS_DIR"],record["directory"],record["filename"])
    f.save(file)
    document_change_time(id)
    
    return response_document(id)

@server.route("/qr", methods = ["POST"])
def qr_code():
    try:
        request_data = request.get_json()
    except:
        return response_error_not_supported()
    
    try:
        id = request_data["document_id"]
    except:
        return response_error_no_document_id()
    
    record = document_find_by_id(id)

    if(not record):
        return response_error_invalid_document_id()
    
    qr_code = qr_create(current_app.config["BASE_URL"], record["directory"], record["filename"])

    return response_qr(qr_code)

