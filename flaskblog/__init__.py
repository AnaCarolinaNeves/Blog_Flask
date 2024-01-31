from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
# Key gerada pelo 'secrets.token_hex(16)'
app.config['SECRET_KEY'] = '218311eaa19b80e1bac2808bf1caef06'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# /// significa que o arquivo será criado no caminho atual do projeto
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# Configurações envio e-mail. flask-email
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# É possível configurar o e-mail e senha colocando-os no environment variables
#app.config['MAIL_USERNAME/PASSWORD'] = os.environ.get('EMAIL_USER/PASSWORD')
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
mail = Mail(app)

# Importando blueprints
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
# Registrando blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)