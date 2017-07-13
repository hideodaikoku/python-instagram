from flask import Flask
app = Flask(__name__, static_url_path='')
app.secret_key = "Pineapples"
from app.routes import index

