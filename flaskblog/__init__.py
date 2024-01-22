from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Key gerada pelo 'secrets.token_hex(16)'
app.config['SECRET_KEY'] = '218311eaa19b80e1bac2808bf1caef06'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# /// significa que o arquivo será criado no caminho atual do projeto
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes