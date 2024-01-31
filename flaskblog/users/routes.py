from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada com sucesso. Seja bem-vindo(a), {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('cadastrar.html', title='Cadastrar', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login inválido. Tente novamente!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash('Para entrar novamente, é necessário realizar o login', 'info')
    return redirect(url_for('main.home'))


@users.route("/conta", methods=['GET', 'POST'])
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
        return redirect(url_for('users.conta'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('conta.html', title='Conta', image_file=image_file, form=form)

@users.route("/usuario/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('usuario_post.html', posts=posts, user=user)

@users.route("/reset_senha", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Um e-mail para redefinir a senha foi enviado, verifique sua caixa de entrada', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_senha.html', title='Resetar Senha', form=form)

@users.route("/reset_senha/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('O token informado está inválido ou expirado', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Sua senha foi redefinida com sucesso. Por favor, realize o login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Resetar Senha', form=form)