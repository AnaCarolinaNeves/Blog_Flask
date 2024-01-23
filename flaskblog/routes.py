from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required


posts = [ 
    {
        'author': 'Joe Doe',
        'title': 'Blog Post 1',
        'content': 'Primeiro post',
        'date_posted': '16 janeiro, 2024'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Segundo post',
        'date_posted': '17 janeiro, 2024'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/sobre")
def sobre():
    return render_template('sobre.html', title='Sobre')


@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada com sucesso. Seja bem-vindo(a), {form.nome.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastrar.html', title='Cadastrar', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login inválido. Tente novamente!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('Para entrar novamente, é necessário realizar o login', 'info')
    return redirect(url_for('home'))

@app.route("/conta", methods=['GET', 'POST'])
@login_required
def conta():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('A sua conta foi atualizada', 'success')
        return redirect(url_for('conta'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('conta.html', title='Conta', image_file=image_file, form=form)