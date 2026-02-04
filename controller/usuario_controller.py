from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from service.usuario_service import UsuarioService
from utils.api_utils import (
    api_error_handler,
    requer_autenticacao,
    requer_admin,
    validar_dados_usuario,
    resposta_padrao
)


usuario_bp = Blueprint("usuario", __name__)

# -------- INÍCIO / PAINEL --------
@usuario_bp.route("/")
def painel():
    if "id_usuario" not in session:
        return redirect(url_for("usuario.login_get"))
    return render_template("painel.html")


# -------- LOGIN --------
@usuario_bp.route("/login")
def login_get():
    return render_template("login.html")


@usuario_bp.route("/login", methods=["POST"])
@api_error_handler  # ← Tratamento de erro automático
def login_post():
    # Aceita tanto form quanto JSON (Postman)
    if request.is_json:
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")
    else:
        email = request.form.get("email")
        senha = request.form.get("senha")

    usuario = UsuarioService.autenticar(email, senha)
    
    if not usuario:
        if request.is_json:
            return resposta_padrao(False, "Email ou senha incorretos!", codigo=401)
        flash("Email ou senha incorretos!", "error")
        return redirect(url_for("usuario.login_get"))

    session["id_usuario"] = usuario["id"]
    session["nome"] = usuario["nome"]
    session["perfil"] = usuario["perfil"]

    if request.is_json:
        # Resposta JSON para Postman/API
        return resposta_padrao(
            True,
            f"Bem-vindo(a), {usuario['nome']}!",
            dados={
                "usuario": {
                    "id": usuario["id"],
                    "nome": usuario["nome"],
                    "perfil": usuario["perfil"]
                }
            },
            codigo=200
        )

    # Resposta HTML normal
    flash(f"Bem-vindo(a), {usuario['nome']}!", "success")
    return redirect(url_for("usuario.painel"))


# -------- LOGOUT --------
@usuario_bp.route("/logout")
def logout():
    session.clear()
    
    if request.is_json:
        return resposta_padrao(True, "Você saiu da sua conta.")
    
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("usuario.login_get"))


# -------- CADASTRO --------
@usuario_bp.route("/cadastro")
def cadastro_get():
    return render_template("cadastro-usuario.html")


@usuario_bp.route("/cadastro-usuario", methods=["POST"])
@api_error_handler  # ← Tratamento de erro automático
def cadastro_post():
    # Aceita tanto form quanto JSON (Postman)
    if request.is_json:
        dados = request.get_json()
    else:
        dados = {
            "nome": request.form.get("nome"),
            "cpf": request.form.get("cpf"),
            "email": request.form.get("email"),
            "idade": request.form.get("idade"),
            "senha": request.form.get("senha"),
            "perfil": request.form.get("perfil", "user")
        }

    # Valida dados (lança erro se inválido)
    validar_dados_usuario(dados)

    status = UsuarioService.cadastrar(dados)
    
    if request.is_json:
        # Resposta JSON para Postman/API
        if status:
            return resposta_padrao(True, "Cadastro realizado com sucesso!", codigo=201)
        return resposta_padrao(False, "Erro ao cadastrar usuário", codigo=400)
    
    # Resposta HTML normal
    if status:
        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("usuario.login_get"))

    flash("Erro ao cadastrar usuário. Tente novamente.", "error")
    return redirect(url_for("usuario.cadastro_get"))


# -------- LISTANIME --------
@usuario_bp.route("/assistindo")
def assistindo():
    return render_template("assistindo.html")


@usuario_bp.route("/concluidos")
def concluidos():
    return render_template("concluidos.html")


@usuario_bp.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")


# -------- ADMIN (USUÁRIOS) --------

@usuario_bp.route("/usuarios/json")
@requer_autenticacao  # ← Verifica login automaticamente
@requer_admin         # ← Verifica se é admin
@api_error_handler    # ← Trata erros
def buscar_usuarios_json():
    usuarios = UsuarioService.listar()
    return resposta_padrao(True, "Usuários listados com sucesso", dados={"usuarios": usuarios})


@usuario_bp.route("/usuarios")
@requer_autenticacao
@requer_admin
@api_error_handler
def buscar_usuarios():
    usuarios = UsuarioService.listar()
    
    if request.is_json:
        return resposta_padrao(True, "Usuários listados", dados={"usuarios": usuarios})
    
    return render_template("usuarios.html", usuarios=usuarios)


@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
@requer_autenticacao
@requer_admin
@api_error_handler
def excluir_usuario(id):
    if UsuarioService.deletar(id):
        return resposta_padrao(True, "Usuário deletado com sucesso.", codigo=200)

    return resposta_padrao(False, "Usuário não encontrado.", codigo=404)


@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
@requer_autenticacao
@api_error_handler
def atualizar_usuario(id):
    # Verifica permissão (mantém lógica original)
    if session["perfil"] != "admin" and session["id_usuario"] != id:
        return resposta_padrao(False, "Acesso negado.", codigo=403)

    dados = request.get_json()
    
    if not dados:
        raise ValueError("Nenhum dado fornecido para atualização")
    
    dados["id"] = id

    if UsuarioService.atualizar(dados):
        return resposta_padrao(True, "Usuário atualizado com sucesso", codigo=200)

    return resposta_padrao(False, "Erro ao atualizar", codigo=400)


@usuario_bp.route("/admin")
@requer_autenticacao
@requer_admin
def admin_area():
    if request.is_json:
        return resposta_padrao(True, "Bem-vindo à área do administrador")
    
    return "Área do administrador"