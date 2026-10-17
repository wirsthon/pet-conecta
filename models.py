from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


def agora():
    return datetime.now(timezone.utc)


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20))
    cidade = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=agora)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    especie = db.Column(db.String(30), nullable=False)
    porte = db.Column(db.String(20))
    idade = db.Column(db.String(30))
    descricao = db.Column(db.Text)
    cidade = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200))
    status = db.Column(db.String(20), default='disponivel')
    criado_em = db.Column(db.DateTime, default=agora)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='animais')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))
