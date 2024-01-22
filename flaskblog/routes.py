from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import CadastroForm, LoginForm
from flaskblog.models import Post, Usuario

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
        hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=hashed_senha)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Conta criada com sucesso. Seja bem-vindo(a), {form.nome.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastrar.html', form=form, titulo='Cadastrar')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'ana@gmail.com' and form.senha.data == '123':
    #         flash('Login feito com sucesso!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login inválido. Tente novamente!', 'danger')
    return render_template('login.html', form=form, titulo='Login')