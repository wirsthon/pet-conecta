from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from extensions import db
from models import Usuario

auth_bp = Blueprint('auth', __name__)

TAMANHO_MIN_SENHA = 6


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        telefone = request.form.get('telefone', '').strip()
        cidade = request.form.get('cidade', '').strip()

        if not nome or not email or not senha:
            flash('Preencha nome, e-mail e senha.', 'erro')
            return render_template('cadastro_usuario.html')

        if len(senha) < TAMANHO_MIN_SENHA:
            flash(f'A senha precisa ter pelo menos {TAMANHO_MIN_SENHA} caracteres.', 'erro')
            return render_template('cadastro_usuario.html')

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'erro')
            return redirect(url_for('auth.cadastro'))

        user = Usuario(nome=nome, email=email, telefone=telefone, cidade=cidade)
        user.set_senha(senha)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado! Faça login.', 'sucesso')
        return redirect(url_for('auth.login'))

    return render_template('cadastro_usuario.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        user = Usuario.query.filter_by(email=email).first()

        if user and user.verifica_senha(senha):
            login_user(user)
            flash(f'Bem-vindo(a), {user.nome}!', 'sucesso')
            return redirect(url_for('views.index'))

        flash('E-mail ou senha inválidos.', 'erro')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.', 'sucesso')
    return redirect(url_for('views.index'))
