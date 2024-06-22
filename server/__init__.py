from flask import Flask
from flask_cors import CORS
import os
from .db import connect

def create_app(userTypes, baseURL, docsdir, mongoURL):
    app = Flask(__name__)
    cors = CORS(app)

    connect()

    from .server import server, setDocsDir, setTypes, setBaseURL
    
    if(not os.path.isdir(docsdir)):
        os.mkdir(docsdir)

    types = userTypes.split(',')
    types.append("QR")
    for type in types:
        typedir = os.path.join(docsdir, type)
        if(not os.path.isdir(typedir)):
            os.mkdir(typedir)
    setDocsDir(docsdir)
    setTypes(types)
    setBaseURL(baseURL)
    
    app.register_blueprint(server, url_prefix='/')

    return app