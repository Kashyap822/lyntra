from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

from src.core.views import core
app.register_blueprint(core)