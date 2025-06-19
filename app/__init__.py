from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicialização do Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Configuração do gerenciador de login
login = LoginManager(app)
login.login_view = "login"  # nome da rota de login


# Registrar o carregador de usuário
@login.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


# Importa rotas e modelos após a configuração
from app import routes, models
