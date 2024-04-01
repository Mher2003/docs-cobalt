from dotenv import load_dotenv
import os
from server import create_app

load_dotenv()

app = create_app(os.environ.get("TYPES"), os.environ.get("BASE_URL"), os.environ.get("DOCS_DIR"), os.environ.get("MONGO_URL"))


if __name__ == '__main__':
    app.config["SECRET_KEY"] = os.environ.get("SECRET")
    app.run(debug=True, port=os.environ.get("PORT"))