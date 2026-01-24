from flask import Blueprint, request, jsonify, session
from service.anime_service import AnimeService

anime_bp = Blueprint("anime", __name__)

# =========================
# LISTAR (COM FILTRO)
# =========================
@anime_bp.route("/animes", methods=["GET"])
def listar_animes():
    usuario_id = session.get("id_usuario")
    status = request.args.get("status")

    if not usuario_id:
        return jsonify([])

    return jsonify(AnimeService.listar(usuario_id, status))


# =========================
# CRIAR
# =========================
@anime_bp.route("/animes", methods=["POST"])
def criar_anime():
    usuario_id = session.get("id_usuario")

    if not usuario_id:
        return jsonify({"erro": "Login obrigatório"}), 401

    dados = request.get_json() or {}
    dados["usuario_id"] = usuario_id

    AnimeService.criar(dados)
    return jsonify({"mensagem": "Anime criado"}), 201


# =========================
# BUSCAR POR ID
# =========================
@anime_bp.route("/animes/<int:id>", methods=["GET"])
def buscar_anime(id):
    anime = AnimeService.buscar_por_id(id)

    if not anime:
        return jsonify({"erro": "Anime não encontrado"}), 404

    return jsonify(anime)


# =========================
# ATUALIZAR
# =========================
@anime_bp.route("/animes/<int:id>", methods=["PUT"])
def atualizar_anime(id):
    usuario_id = session.get("id_usuario")

    if not usuario_id:
        return jsonify({"erro": "Login obrigatório"}), 401

    dados = request.get_json() or {}
    AnimeService.atualizar(id, dados)

    return jsonify({"mensagem": "Anime atualizado"})


# =========================
# DELETAR
# =========================
@anime_bp.route("/animes/<int:id>", methods=["DELETE"])
def deletar_anime(id):
    usuario_id = session.get("id_usuario")

    if not usuario_id:
        return jsonify({"erro": "Login obrigatório"}), 401

    AnimeService.deletar(id)
    return jsonify({"mensagem": "Anime removido"})
