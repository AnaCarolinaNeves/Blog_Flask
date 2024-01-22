from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# Key gerada pelo 'secrets.token_hex(16)'
app.config['SECRET_KEY'] = '218311eaa19b80e1bac2808bf1caef06'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# /// significa que o arquivo será criado no caminho atual do projeto
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskblog import routes