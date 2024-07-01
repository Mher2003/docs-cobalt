import os
from dotenv import load_dotenv
from server import create_app, init_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.config["SECRET_KEY"] = os.environ.get("SECRET")
    app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")
    app.config["PASSWORD_HASHED"]=os.environ.get("PASSWORD_HASHED")
    app.config["DIRECTORIES"]=os.environ.get("DIRECTORIES")
    app.config["BASE_URL"]=os.environ.get("BASE_URL")
    app.config["DOCS_DIR"]=os.environ.get("DOCS_DIR")
    app.config["MONGO_URL"]=os.environ.get("MONGO_URL")

    init_app(app)

    app.run(debug=False, port=os.environ.get("PORT"))