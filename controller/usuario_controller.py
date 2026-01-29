from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from service.usuario_service import UsuarioService
import re

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/")
def painel():
    if "id_usuario" not in session:
        return redirect(url_for("usuario.login_get"))
    return render_template("painel.html")

@usuario_bp.route("/login")
def login_get():
    return render_template("login.html")

@usuario_bp.route("/login", methods=["POST"])
def login_post():
    usuario = UsuarioService.autenticar(
        request.form.get("email"),
        request.form.get("senha")
    )

    if not usuario:
        return render_template("login.html", erro="Email ou senha inválidos")

    session["id_usuario"] = usuario["id"]
    session["nome"] = usuario["nome"]
    session["perfil"] = usuario["perfil"]

    return redirect(url_for("usuario.painel"))

@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("usuario.login_get"))

@usuario_bp.route("/cadastro")
def cadastro_get():
    return render_template("cadastro-usuario.html")

@usuario_bp.route("/cadastro-usuario", methods=["POST"])
def cadastro_post():
    cpf = re.sub(r"\D", "", request.form.get("cpf"))

    dados = {
        "nome": request.form.get("nome"),
        "cpf": cpf,
        "email": request.form.get("email"),
        "idade": request.form.get("idade"),
        "senha": request.form.get("senha"),
        "perfil": request.form.get("perfil", "user")
    }

    if UsuarioService.cadastrar(dados):
        return redirect(url_for("usuario.login_get"))

    return "Erro ao cadastrar usuário", 400

@usuario_bp.route("/usuarios")
def buscar_usuarios():
    if session.get("perfil") != "admin":
        return "Acesso negado", 403

    return render_template(
        "usuarios.html",
        usuarios=UsuarioService.listar()
    )

@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
def excluir_usuario(id):
    if session.get("perfil") != "admin":
        return "Acesso negado", 403

    return jsonify({"ok": UsuarioService.deletar(id)})

@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
def atualizar_usuario(id):
    dados = request.get_json()
    dados["id"] = id

    return jsonify({"ok": UsuarioService.atualizar(dados)})
