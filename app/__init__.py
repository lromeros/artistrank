from flask import Flask

app = Flask(__name__)
app.secret_key = b'CHANGE THIS'  # TODO

from app import views
