import uuid
from flask import Flask

app = Flask(__name__)
app.secret_key = uuid.uuid4().bytes

from app import views
