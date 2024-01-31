from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('O nome de usuário já está sendo utilizado. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('O email já está sendo utilizado. Por favor, escolha outro.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Continuar conectado')
    submit = SubmitField('Entrar')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Atualizar imagem de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('O nome de usuário já está sendo utilizado. Por favor, escolha outro.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('O email já está sendo utilizado. Por favor, escolha outro.')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Redefinição de senha')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Nenhum usuário encontrado com este email. Verifique e tente novamente.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinição de senha')