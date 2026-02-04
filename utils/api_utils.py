"""
Utilitários para tratamento de erros em API REST
Use estes decorators e funções para melhorar suas rotas
"""
from functools import wraps
from flask import jsonify, request, session
import traceback


def api_error_handler(f):
    """
    Decorator para tratamento automático de erros em rotas API
    Retorna JSON em caso de erro
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"erro": str(e), "tipo": "ValueError"}), 400
        except KeyError as e:
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}", "tipo": "KeyError"}), 400
        except Exception as e:
            print(f"Erro não tratado: {traceback.format_exc()}")
            return jsonify({
                "erro": "Erro interno do servidor",
                "detalhes": str(e),
                "tipo": type(e).__name__
            }), 500
    return decorated_function


def requer_autenticacao(f):
    """
    Decorator que verifica se o usuário está autenticado
    Retorna JSON se não estiver
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "id_usuario" not in session:
            # Verifica se é requisição JSON (Postman/API)
            if request.is_json or request.headers.get("Content-Type") == "application/json":
                return jsonify({"erro": "Não autenticado", "codigo": "AUTH_REQUIRED"}), 401
            # Senão, mantém comportamento original (redirect)
            from flask import redirect, url_for
            return redirect(url_for("usuario.login_get"))
        return f(*args, **kwargs)
    return decorated_function


def requer_admin(f):
    """
    Decorator que verifica se o usuário é admin
    Retorna JSON se não for
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("perfil") != "admin":
            if request.is_json or request.headers.get("Content-Type") == "application/json":
                return jsonify({"erro": "Acesso negado. Apenas administradores.", "codigo": "FORBIDDEN"}), 403
            return "Acesso negado. Área de administração.", 403
        return f(*args, **kwargs)
    return decorated_function


def validar_dados_usuario(dados):
    """
    Valida dados de cadastro de usuário
    Lança ValueError se algum dado for inválido
    """
    campos_obrigatorios = ["nome", "email", "senha"]
    
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            raise ValueError(f"Campo '{campo}' é obrigatório")
    
    if len(dados.get("senha", "")) < 6:
        raise ValueError("Senha deve ter no mínimo 6 caracteres")
    
    if "@" not in dados.get("email", ""):
        raise ValueError("Email inválido")
    
    return True


def resposta_padrao(sucesso=True, mensagem="", dados=None, codigo=200):
    """
    Cria uma resposta JSON padronizada
    
    Uso:
        return resposta_padrao(True, "Usuário criado", {"id": "123"}, 201)
    """
    resposta = {
        "sucesso": sucesso,
        "mensagem": mensagem
    }
    
    if dados is not None:
        resposta["dados"] = dados
    
    return jsonify(resposta), codigo