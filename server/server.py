from flask import Blueprint,render_template, request, make_response
import os, datetime
from .auth import login, checkSession, deleteSession
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
    return "Cobalt Docs V1.0"

@server.route('/', methods= ['POST'])
def api():
    return "Cobalt Docs API V1.0"

@server.route('/login', methods=['POST'])
def log():
    password = request.form["password"]
    sessionID = login(password)
    if(not sessionID):
        return "Invalid Session"
    response = make_response()
    response.set_cookie("sessionID", sessionID)
    return response

@server.route('/logout', methods=['POST'])
def logout():
    sessionID = request.cookies.get("sessionID")
    deleteSession(sessionID)
    response = make_response()
    response.set_cookie("sessionID", "")
    return response

@server.route('/add', methods = ['POST'])
def add():
    sessionID = request.cookies.get("sessionID")
    if(not checkSession(sessionID)): # Check auth
        response = make_response("Invalid Session", 200)
        response.mimetype = "text/plain"
        response.set_cookie("sessionID", "")
        return response
    id = addFile(request.form["type"],request.form["file"])
    if(not id):
        return "Filename exists"
    qr = CreateQR(baseURL, docsdir, id, request.form["type"], request.form["file"])
    return id

@server.route('/upload', methods = ['POST'])
def upload():
    sessionID = request.cookies.get("sessionID")
    if(not checkSession(sessionID)): # Check auth
        response = make_response("Invalid Session", 200)
        response.mimetype = "text/plain"
        response.set_cookie("sessionID", "")
        return response
    f,id = request.files['file'],request.form["id"]
    record = findID(id)
    if((not record) or (not f)):
        return "File doesn't exists"
    file = os.path.join(docsdir,record["type"],record["file"])
    f.save(file)
    change_time(id)
    return "True"