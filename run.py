from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Para instalar os pacotes -> pip install -r requirements.txt
