from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from service.usuario_service import UsuarioService


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
def login_post():
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = UsuarioService.autenticar(email, senha)
    if not usuario:
        return render_template("login.html", erro="Email ou senha inválidos")


    session["id_usuario"] = usuario["id"]
    session["nome"] = usuario["nome"]
    session["perfil"] = usuario["perfil"]

    return redirect(url_for("usuario.painel"))


# -------- LOGOUT --------
@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("usuario.login_get"))


# -------- CADASTRO --------
@usuario_bp.route("/cadastro")
def cadastro_get():
    return render_template("cadastro-usuario.html")


@usuario_bp.route("/cadastro-usuario", methods=["POST"])
def cadastro_post():
    dados = {
        "nome": request.form.get("nome"),
        "cpf": request.form.get("cpf"),
        "email": request.form.get("email"),
        "idade": request.form.get("idade"),
        "senha": request.form.get("senha"),
        "perfil": request.form.get("perfil", "user")
    }

    status = UsuarioService.cadastrar(dados)
    if status:
        return redirect(url_for("usuario.login_get"))

    return "Erro ao cadastrar usuário", 400


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
def buscar_usuarios_json():
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401
    if session["perfil"] != "admin":
        return "Acesso negado. Área de administração.", 401

    return jsonify(UsuarioService.listar())


@usuario_bp.route("/usuarios")
def buscar_usuarios():
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401
    if session["perfil"] != "admin":
        return "Acesso negado. Área de administração.", 401

    usuarios = UsuarioService.listar()
    return render_template("usuarios.html", usuarios=usuarios)


@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
def excluir_usuario(id):
    if session.get("perfil") != "admin":
        return "Acesso negado. Apenas administradores podem deletar usuários.", 403

    if UsuarioService.deletar(id):
        return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200

    return jsonify({"erro": "Usuário não encontrado."}), 404


@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
def atualizar_usuario(id):
    if "id_usuario" not in session:
        return "Acesso negado. Faça login.", 401

    if session["perfil"] != "admin" and session["id_usuario"] != id:
        return "Acesso negado.", 403

    dados = request.get_json()
    dados["id"] = id

    if UsuarioService.atualizar(dados):
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200

    return jsonify({"erro": "Erro ao atualizar"}), 400
@usuario_bp.route("/admin")
def admin_area():
    if session.get("perfil") != "admin":
        return "Acesso negado", 403

    return "Área do administrador"

