import os
from flask import Flask, current_app
from flask_cors import CORS
from flask_ipban import IpBan
from .server import server, set_ip_ban
from .db import mongodb_connect


def create_app():
    app = Flask(__name__)
    
    return app

def init_app(app):
    CORS(app)

    ip_ban = IpBan(ban_seconds=3600, ban_count=3)
    ip_ban.init_app(app)

    with app.app_context():
        mongodb_connect("mongodb://"+current_app.config["MONGO_URL"])
    
        if(not os.path.isdir(current_app.config["DOCS_DIR"])):
            os.mkdir(current_app.config["DOCS_DIR"])

        directories_string = current_app.config["DIRECTORIES"]
        directories = directories_string.split(',')
        for dir in directories:
            directory_path = os.path.join(current_app.config["DOCS_DIR"], dir)
            if(not os.path.isdir(directory_path)):
                os.mkdir(directory_path)
    
        set_ip_ban(ip_ban)
        app.register_blueprint(server, url_prefix='/')

    return app