#-*- coding: utf-8 -*-
import os 
from flask import Flask, render_template
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from .config.Config import api, db, jwt
from .config.DBConfig import MySQLConfig
from .controller.controller import register_namespaces
import warnings

app = Flask(__name__)

CORS(app)

app.config['JSON_AS_ASCII'] = False

app.config.from_object(MySQLConfig)

'''JWT 설정'''
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30 * 24 *  60 * 60
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 
''''''
# JST SECRET KEY
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

# SECRET_KEY 설정
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


api.init_app(app)
db.init_app(app)
jwt.init_app(app)
register_namespaces(api)
socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route('/map/preview')
# def previewMap():
#     return render_template('movie.html')

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    app.run()