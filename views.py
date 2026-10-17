import os
from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models import Animal

views_bp = Blueprint('views', __name__)

# extensões de imagem aceitas no upload
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp'}


def extensao_permitida(nome_arquivo):
    return ('.' in nome_arquivo and
            nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS)


@views_bp.route('/')
def index():
    disponiveis = Animal.query.filter_by(status='disponivel').count()
    adotados = Animal.query.filter_by(status='adotado').count()
    ultimos = (Animal.query
               .filter_by(status='disponivel')
               .order_by(Animal.criado_em.desc())
               .limit(6)
               .all())
    return render_template('index.html',
                           total_animais=disponiveis,
                           total_adotados=adotados,
                           ultimos=ultimos)


@views_bp.route('/animais')
def lista_animais():
    cidade = request.args.get('cidade', '')
    especie = request.args.get('especie', '')
    porte = request.args.get('porte', '')

    q = Animal.query.filter_by(status='disponivel')

    if cidade:
        q = q.filter(Animal.cidade.ilike(f'%{cidade}%'))
    if especie:
        q = q.filter_by(especie=especie)
    if porte:
        q = q.filter_by(porte=porte)

    animais = q.order_by(Animal.criado_em.desc()).all()
    return render_template('lista_animais.html',
                           animais=animais,
                           cidade=cidade,
                           especie=especie,
                           porte=porte)


@views_bp.route('/animal/<int:animal_id>')
def detalhe_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template('detalhe_animal.html', animal=animal)


@views_bp.route('/cadastrar-animal', methods=['GET', 'POST'])
@login_required
def cadastrar_animal():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        especie = request.form.get('especie', '').strip()
        porte = request.form.get('porte', '')
        idade = request.form.get('idade', '')
        descricao = request.form.get('descricao', '')
        cidade = request.form.get('cidade', '').strip()

        # campos obrigatórios (o "required" do HTML pode ser contornado)
        if not nome or not especie or not cidade:
            flash('Preencha nome, espécie e cidade.', 'erro')
            return render_template('cadastro_animal.html')

        foto_nome = None
        foto = request.files.get('foto')
        if foto and foto.filename:
            if not extensao_permitida(foto.filename):
                flash('Formato de imagem inválido. Use PNG, JPG, JPEG ou WEBP.', 'erro')
                return render_template('cadastro_animal.html')

            foto_nome = secure_filename(f"{datetime.now().timestamp()}_{foto.filename}")
            pasta = current_app.config['UPLOAD_FOLDER']
            os.makedirs(pasta, exist_ok=True)  # cria a pasta se ainda não existir
            foto.save(os.path.join(pasta, foto_nome))

        novo = Animal(
            nome=nome, especie=especie, porte=porte, idade=idade,
            descricao=descricao, cidade=cidade, foto=foto_nome,
            usuario_id=current_user.id
        )
        db.session.add(novo)
        db.session.commit()
        flash('Animal cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('views.lista_animais'))

    return render_template('cadastro_animal.html')


@views_bp.route('/animal/<int:animal_id>/adotar', methods=['POST'])
@login_required
def marcar_adotado(animal_id):
    animal = Animal.query.get_or_404(animal_id)

    if animal.usuario_id != current_user.id:
        flash('Você não tem permissão.', 'erro')
        return redirect(url_for('views.lista_animais'))

    animal.status = 'adotado'
    db.session.commit()
    flash(f'{animal.nome} foi marcado como adotado!', 'sucesso')
    return redirect(url_for('views.detalhe_animal', animal_id=animal.id))


@views_bp.route('/meus-animais')
@login_required
def meus_animais():
    animais = (Animal.query
               .filter_by(usuario_id=current_user.id)
               .order_by(Animal.criado_em.desc())
               .all())
    return render_template('meus_animais.html', animais=animais)