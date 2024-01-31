class Config:
    # Key gerada pelo 'secrets.token_hex(16)'
    SECRET_KEY = '218311eaa19b80e1bac2808bf1caef06'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # /// significa que o arquivo será criado no caminho atual do projeto

    # Configurações envio e-mail. flask-email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # É possível configurar o e-mail e senha colocando-os no environment variables
    #app.config['MAIL_USERNAME/PASSWORD'] = os.environ.get('EMAIL_USER/PASSWORD')
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''