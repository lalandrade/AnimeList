from flask import Blueprint, request, jsonify, session
from repository.anime_repository import AnimeRepository

anime_bp = Blueprint("anime", __name__)

# LISTAR
@anime_bp.route("/animes", methods=["GET"])
def listar_animes():
    usuario_id = session.get("id_usuario") or 1  # TEMPORÁRIO
    return jsonify(AnimeRepository.listar(usuario_id))


# CRIAR
@anime_bp.route("/animes", methods=["POST"])
def criar_anime():
    usuario_id = session.get("id_usuario")

    if not usuario_id:
        return jsonify({"erro": "Você precisa estar logado"}), 401

    dados = request.get_json()
    dados["usuario_id"] = usuario_id

    AnimeRepository.adicionar(dados)
    return jsonify({"mensagem": "Anime criado"}), 201





# BUSCAR POR ID
@anime_bp.route("/animes/<int:id>", methods=["GET"])
def buscar_anime(id):
    return jsonify(AnimeRepository.buscar_por_id(id))


# ATUALIZAR
@anime_bp.route("/animes/<int:id>", methods=["PUT"])
def atualizar_anime(id):
    dados = request.get_json()
    AnimeRepository.atualizar(id, dados)
    return jsonify({"mensagem": "Anime atualizado"})


# DELETAR
@anime_bp.route("/animes/<int:id>", methods=["DELETE"])
def deletar_anime(id):
    AnimeRepository.deletar(id)
    return jsonify({"mensagem": "Anime removido"})
