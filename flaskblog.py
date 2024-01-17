from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)