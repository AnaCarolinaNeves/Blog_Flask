from datetime import datetime
from flaskblog import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    icone_usuario = db.Column(db.String(20), nullable=False, default='default.jpg')
    senha = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='autor', lazy=True)

    def __repr__(self):
        return f"Usuario('{self.nome}', '{self.email}', '{self.icone_usuario}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    conteudo = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.titulo}', '{self.data_post}')"