import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/conta", methods=['GET', 'POST'])
@login_required
def conta():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            old_pic = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_pic != 'default.jpg':
                os.remove(os.path.join(app.root_path, 'static/profile_pics', old_pic))
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

@app.route("/post/novo", methods=['GET', 'POST'])
@login_required
def novo_post():
    form = PostForm()
    if form.validate_on_submit():

        flash('Post publicado com sucesso', 'success')
        return redirect(url_for('home'))
    return render_template('criar_post.html', title='Novo Post', form=form)