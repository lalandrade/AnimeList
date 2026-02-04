"""
Testes para o módulo de Usuários
Cobertura: Controller, Service, Repository
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, session
from controller.usuario_controller import usuario_bp
from service.usuario_service import UsuarioService
from repository.usuario_repository import UsuarioRepository
import json


@pytest.fixture
def app():
    """Cria aplicação Flask para testes"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(usuario_bp)
    return app


@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()


@pytest.fixture
def logged_client(client):
    """Cliente já autenticado"""
    # Cadastra usuário de teste
    client.post('/cadastro-usuario', 
        json={
            'nome': 'Teste User',
            'cpf': '12345678900',
            'email': 'teste@email.com',
            'senha': 'senha123',
            'perfil': 'user'
        }
    )
    
    # Faz login
    client.post('/login',
        json={
            'email': 'teste@email.com',
            'senha': 'senha123'
        }
    )
    
    return client


@pytest.fixture
def admin_client(client):
    """Cliente autenticado como admin"""
    # Cadastra admin
    client.post('/cadastro-usuario',
        json={
            'nome': 'Admin User',
            'cpf': '99999999999',
            'email': 'admin@email.com',
            'senha': 'admin123',
            'perfil': 'admin'
        }
    )
    
    # Faz login
    client.post('/login',
        json={
            'email': 'admin@email.com',
            'senha': 'admin123'
        }
    )
    
    return client


# =========================
# TESTES DE CADASTRO
# =========================

class TestCadastro:
    """Testes do endpoint de cadastro"""
    
    def test_cadastro_sucesso(self, client):
        """Testa cadastro com dados válidos"""
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'João Silva',
                'cpf': '11111111111',
                'email': 'joao@email.com',
                'senha': 'senha123',
                'perfil': 'user'
            }
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['sucesso'] == True
        assert 'Cadastro realizado com sucesso' in data['mensagem']
    
    def test_cadastro_sem_nome(self, client):
        """Testa cadastro sem nome"""
        response = client.post('/cadastro-usuario',
            json={
                'cpf': '11111111111',
                'email': 'joao@email.com',
                'senha': 'senha123'
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'nome' in data['erro'].lower()
    
    def test_cadastro_sem_email(self, client):
        """Testa cadastro sem email"""
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'João Silva',
                'cpf': '11111111111',
                'senha': 'senha123'
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in data['erro'].lower()
    
    def test_cadastro_senha_curta(self, client):
        """Testa cadastro com senha muito curta"""
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'João Silva',
                'email': 'joao@email.com',
                'senha': '123'
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'senha' in data['erro'].lower()
    
    def test_cadastro_email_invalido(self, client):
        """Testa cadastro com email inválido"""
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'João Silva',
                'email': 'email_invalido',
                'senha': 'senha123'
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in data['erro'].lower()


# =========================
# TESTES DE LOGIN
# =========================

class TestLogin:
    """Testes do endpoint de login"""
    
    def test_login_sucesso(self, client):
        """Testa login com credenciais válidas"""
        # Primeiro cadastra
        client.post('/cadastro-usuario',
            json={
                'nome': 'Maria',
                'email': 'maria@email.com',
                'senha': 'senha123'
            }
        )
        
        # Depois faz login
        response = client.post('/login',
            json={
                'email': 'maria@email.com',
                'senha': 'senha123'
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['sucesso'] == True
        assert 'dados' in data
        assert 'usuario' in data['dados']
    
    def test_login_senha_errada(self, client):
        """Testa login com senha incorreta"""
        # Cadastra
        client.post('/cadastro-usuario',
            json={
                'nome': 'Pedro',
                'email': 'pedro@email.com',
                'senha': 'senha123'
            }
        )
        
        # Tenta login com senha errada
        response = client.post('/login',
            json={
                'email': 'pedro@email.com',
                'senha': 'senha_errada'
            }
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['sucesso'] == False
    
    def test_login_usuario_inexistente(self, client):
        """Testa login com usuário que não existe"""
        response = client.post('/login',
            json={
                'email': 'naoexiste@email.com',
                'senha': 'senha123'
            }
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['sucesso'] == False


# =========================
# TESTES DE LOGOUT
# =========================

class TestLogout:
    """Testes do endpoint de logout"""
    
    def test_logout_sucesso(self, logged_client):
        """Testa logout de usuário autenticado"""
        response = logged_client.get('/logout')
        
        assert response.status_code in [200, 302]  # 302 se redirecionar
        
        # Verifica que não consegue mais acessar rota protegida
        response = logged_client.get('/usuarios/json')
        assert response.status_code in [401, 403]


# =========================
# TESTES DE LISTAGEM (ADMIN)
# =========================

class TestListarUsuarios:
    """Testes de listagem de usuários"""
    
    def test_listar_usuarios_admin(self, admin_client):
        """Admin consegue listar usuários"""
        response = admin_client.get('/usuarios/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['sucesso'] == True
        assert 'dados' in data
        assert 'usuarios' in data['dados']
    
    def test_listar_usuarios_sem_permissao(self, logged_client):
        """Usuário comum não consegue listar"""
        response = logged_client.get('/usuarios/json')
        
        assert response.status_code == 403
    
    def test_listar_usuarios_sem_login(self, client):
        """Sem login não consegue listar"""
        response = client.get('/usuarios/json')
        
        assert response.status_code == 401


# =========================
# TESTES DE ATUALIZAÇÃO
# =========================

class TestAtualizarUsuario:
    """Testes de atualização de usuário"""
    
    def test_atualizar_proprio_usuario(self, logged_client):
        """Usuário atualiza próprios dados"""
        # Pega ID do usuário logado
        with logged_client.session_transaction() as sess:
            user_id = sess.get('id_usuario')
        
        response = logged_client.put(f'/usuarios/{user_id}',
            json={
                'nome': 'Nome Atualizado',
                'email': 'novo@email.com'
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['sucesso'] == True
    
    def test_atualizar_sem_dados(self, logged_client):
        """Tenta atualizar sem enviar dados"""
        with logged_client.session_transaction() as sess:
            user_id = sess.get('id_usuario')
        
        response = logged_client.put(f'/usuarios/{user_id}',
            json={}
        )
        
        assert response.status_code == 400


# =========================
# TESTES DE EXCLUSÃO (ADMIN)
# =========================

class TestDeletarUsuario:
    """Testes de exclusão de usuário"""
    
    def test_deletar_usuario_admin(self, admin_client, client):
        """Admin consegue deletar usuário"""
        # Cria usuário para deletar
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'Para Deletar',
                'email': 'deletar@email.com',
                'senha': 'senha123'
            }
        )
        
        # Pega lista de usuários para encontrar ID
        response = admin_client.get('/usuarios/json')
        data = json.loads(response.data)
        usuarios = data['dados']['usuarios']
        
        # Encontra usuário criado
        usuario_deletar = next(
            (u for u in usuarios if u['email'] == 'deletar@email.com'),
            None
        )
        
        if usuario_deletar:
            # Deleta
            response = admin_client.delete(f'/usuarios/{usuario_deletar["id"]}')
            assert response.status_code == 200
    
    def test_deletar_sem_permissao(self, logged_client):
        """Usuário comum não consegue deletar"""
        response = logged_client.delete('/usuarios/fake-id')
        
        assert response.status_code == 403


# =========================
# TESTES DE SERVICE
# =========================

class TestUsuarioService:
    """Testes da camada de serviço"""
    
    def test_validar_dados_usuario_valido(self):
        """Valida dados de usuário corretos"""
        from utils.api_utils import validar_dados_usuario
        
        dados = {
            'nome': 'Teste',
            'email': 'teste@email.com',
            'senha': 'senha123'
        }
        
        assert validar_dados_usuario(dados) == True
    
    def test_validar_dados_sem_email(self):
        """Valida rejeição de dados sem email"""
        from utils.api_utils import validar_dados_usuario
        
        dados = {
            'nome': 'Teste',
            'senha': 'senha123'
        }
        
        with pytest.raises(ValueError):
            validar_dados_usuario(dados)
    
    def test_validar_senha_curta(self):
        """Valida rejeição de senha curta"""
        from utils.api_utils import validar_dados_usuario
        
        dados = {
            'nome': 'Teste',
            'email': 'teste@email.com',
            'senha': '123'
        }
        
        with pytest.raises(ValueError):
            validar_dados_usuario(dados)


# =========================
# TESTES DE INTEGRAÇÃO
# =========================

class TestFluxoCompleto:
    """Testa fluxo completo de uso"""
    
    def test_fluxo_usuario_completo(self, client):
        """Testa: Cadastro → Login → Atualizar → Logout"""
        
        # 1. Cadastro
        response = client.post('/cadastro-usuario',
            json={
                'nome': 'Fluxo Teste',
                'email': 'fluxo@email.com',
                'senha': 'senha123'
            }
        )
        assert response.status_code == 201
        
        # 2. Login
        response = client.post('/login',
            json={
                'email': 'fluxo@email.com',
                'senha': 'senha123'
            }
        )
        assert response.status_code == 200
        
        # 3. Atualizar
        with client.session_transaction() as sess:
            user_id = sess.get('id_usuario')
        
        response = client.put(f'/usuarios/{user_id}',
            json={'nome': 'Nome Modificado'}
        )
        assert response.status_code == 200
        
        # 4. Logout
        response = client.get('/logout')
        assert response.status_code in [200, 302]


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=controller', '--cov=service', '--cov=repository', '--cov-report=html'])