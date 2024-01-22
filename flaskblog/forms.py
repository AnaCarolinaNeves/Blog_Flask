from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import Usuario

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirma_senha = PasswordField('Confirma senha', validators=[DataRequired(), EqualTo('senha')])

    submit = SubmitField('Cadastrar')

    def valida_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('O email já está sendo utilizado');

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    guardar_login = BooleanField('Continuar conectado')
    
    submit = SubmitField('Entrar')