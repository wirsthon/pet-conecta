import pytest
from app import create_app
from extensions import db
from models import Usuario, Animal


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_cadastro_usuario(client):
    response = client.post('/cadastro', data={
        'nome': 'Usuario Teste',
        'email': 'teste@teste.com',
        'senha': 'senha123',
        'telefone': '123456789',
        'cidade': 'Aparecida'
    }, follow_redirects=True)
    
    assert b'Cadastro realizado' in response.data


def test_login_usuario(client):
    client.post('/cadastro', data={
        'nome': 'Usuario Teste',
        'email': 'teste@teste.com',
        'senha': 'senha123',
        'telefone': '123456789',
        'cidade': 'Aparecida'
    })
    
    response = client.post('/login', data={
        'email': 'teste@teste.com',
        'senha': 'senha123'
    }, follow_redirects=True)
    
    assert b'Bem-vindo' in response.data


def test_tentar_adotar_sem_permissao(client):
    client.post('/cadastro', data={'nome': 'Dono', 'email': 'dono@teste.com', 'senha': '123456', 'telefone': '', 'cidade': 'A'})
    client.post('/cadastro', data={'nome': 'Invasor', 'email': 'invasor@teste.com', 'senha': '123456', 'telefone': '', 'cidade': 'B'})
    
    client.post('/login', data={'email': 'dono@teste.com', 'senha': '123456'})
    client.post('/cadastrar-animal', data={
        'nome': 'Rex', 'especie': 'Cachorro', 'porte': 'Médio', 
        'idade': 'Adulto', 'descricao': 'Teste', 'cidade': 'A'
    })
    
    client.get('/logout')
    client.post('/login', data={'email': 'invasor@teste.com', 'senha': '123456'})
    
    response = client.post('/animal/1/adotar', follow_redirects=True)
    
    assert b'permiss' in response.data