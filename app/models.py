from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(
        db.Boolean, default=False
    )  # False = usuário comum, True=admin
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)  # Hash da senha
    mudaSenha = db.Column(db.Boolean, default=False)
    liberacao = db.Column(db.Boolean, default=True)

    perfil = db.relationship("Perfil", backref="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"


class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
    nome = db.Column(db.String(50))
    contato = db.Column(db.String(11))
    foto = db.Column(db.String(100))

    def __repr__(self):
        return f"<Perfil {self.nome}>"
