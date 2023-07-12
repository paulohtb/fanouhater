from flask import Flask

app = Flask(__name__)
UPLOAD_FOLDER = './data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from fanorhater import routes
