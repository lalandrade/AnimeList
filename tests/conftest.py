"""
Configuração de fixtures para testes
Coloque este arquivo em: tests/conftest.py

SOLUÇÃO DEFINITIVA: Usa context manager para manter sessão
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Cria a aplicação Flask para testes"""
    # Importa a função de criação do app
    from app import create_app  # Ajuste conforme sua estrutura
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key-12345'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # IMPORTANTE: Permite cookies em redirects
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    
    return app


@pytest.fixture
def client(app):
    """Cliente de teste básico"""
    return app.test_client()


@pytest.fixture
def admin_client(app):
    """
    Cliente autenticado como ADMIN
    USA WITH para manter contexto de sessão
    """
    client = app.test_client()
    
    # Dentro do with, a sessão persiste
    with client:
        # 1. Cadastra admin
        client.post('/cadastro-usuario', 
            json={
                'nome': 'Admin Test',
                'email': 'admin@test.com',
                'cpf': '99999999999',
                'idade': 30,
                'senha': 'admin123',
                'perfil': 'admin'
            }
        )
        
        # 2. Faz login
        client.post('/login',
            json={
                'email': 'admin@test.com',
                'senha': 'admin123'
            }
        )
        
        # Retorna dentro do contexto
        yield client


@pytest.fixture
def logged_client(app):
    """
    Cliente autenticado como USER
    USA WITH para manter contexto de sessão
    """
    client = app.test_client()
    
    with client:
        # 1. Cadastra usuário
        client.post('/cadastro-usuario',
            json={
                'nome': 'User Test',
                'email': 'user@test.com',
                'cpf': '11111111111',
                'idade': 25,
                'senha': 'user123'
            }
        )
        
        # 2. Faz login
        client.post('/login',
            json={
                'email': 'user@test.com',
                'senha': 'user123'
            }
        )
        
        yield client


# ==========================================
# ALTERNATIVA: Fixtures que injetam headers
# ==========================================

@pytest.fixture
def admin_client_alt(app):
    """
    Cliente admin usando Authorization header
    Use se as fixtures acima não funcionarem
    """
    client = app.test_client()
    
    # Cadastra admin
    client.post('/cadastro-usuario', 
        json={
            'nome': 'Admin Test',
            'email': 'admin@test.com',
            'cpf': '99999999999',
            'idade': 30,
            'senha': 'admin123',
            'perfil': 'admin'
        }
    )
    
    # Não precisa fazer login, usa header
    # Wrapper que adiciona header automaticamente
    class AuthClient:
        def __init__(self, client):
            self._client = client
            
        def get(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer admin-id:admin'
            return self._client.get(*args, **kwargs)
            
        def post(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer admin-id:admin'
            return self._client.post(*args, **kwargs)
            
        def put(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer admin-id:admin'
            return self._client.put(*args, **kwargs)
            
        def delete(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer admin-id:admin'
            return self._client.delete(*args, **kwargs)
    
    return AuthClient(client)


@pytest.fixture
def logged_client_alt(app):
    """Cliente user usando Authorization header"""
    client = app.test_client()
    
    client.post('/cadastro-usuario',
        json={
            'nome': 'User Test',
            'email': 'user@test.com',
            'cpf': '11111111111',
            'idade': 25,
            'senha': 'user123'
        }
    )
    
    class AuthClient:
        def __init__(self, client):
            self._client = client
            
        def get(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer user-id:user'
            return self._client.get(*args, **kwargs)
            
        def post(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer user-id:user'
            return self._client.post(*args, **kwargs)
            
        def put(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer user-id:user'
            return self._client.put(*args, **kwargs)
            
        def delete(self, *args, **kwargs):
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer user-id:user'
            return self._client.delete(*args, **kwargs)
        
        def session_transaction(self):
            """Compatibilidade"""
            return self._client.session_transaction()
    
    return AuthClient(client)