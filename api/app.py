import os
import sys
from flask import Flask

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from api.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
