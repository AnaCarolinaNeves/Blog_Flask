from flask import Flask, render_template, url_for, flash, redirect
from forms import CadastroForm, LoginForm

app = Flask(__name__)

# Key gerada pelo 'secrets.token_hex(16)'
app.config['SECRET_KEY'] = '218311eaa19b80e1bac2808bf1caef06'

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