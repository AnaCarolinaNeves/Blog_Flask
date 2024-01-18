from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import CadastroForm, LoginForm

app = Flask(__name__)
# Key gerada pelo 'secrets.token_hex(16)'
app.config['SECRET_KEY'] = '218311eaa19b80e1bac2808bf1caef06'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# /// significa que o arquivo será criado no caminho atual do projeto
db = SQLAlchemy(app)

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

posts = [ 
    {
        'autor': 'Joe Doe',
        'titulo': 'Blog Post 1',
        'conteudo': 'Primeiro post',
        'data_post': '16 janeiro, 2024'
    },
    {
        'autor': 'Jane Doe',
        'titulo': 'Blog Post 2',
        'conteudo': 'Segundo post',
        'data_post': '17 janeiro, 2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = CadastroForm()
    if form.validate_on_submit():
        flash(f'Conta criada com sucesso. Seja bem-vindo(a), {form.nome.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('cadastrar.html', form=form, titulo='Cadastrar')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'ana@gmail.com' and form.senha.data == '123':
            flash('Login feito com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login inválido. Tente novamente!', 'danger')
    return render_template('login.html', form=form, titulo='Login')

if __name__ == '__main__':
    app.run(debug=True)