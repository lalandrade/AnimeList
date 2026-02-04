from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from service.anime_service import AnimeService
from utils.api_utils import (
    api_error_handler,
    requer_autenticacao,
    resposta_padrao
)

anime_bp = Blueprint("anime", __name__)


# =========================
# LISTAR (COM FILTRO)
# =========================
@anime_bp.route("/animes", methods=["GET"])
@requer_autenticacao
@api_error_handler
def listar_animes():
    """
    Lista animes do usuário logado
    Query params: ?status=assistindo|concluido|favorito
    """
    usuario_id = session.get("id_usuario")
    status = request.args.get("status")

    animes = AnimeService.listar(usuario_id, status)
    
    if request.is_json or request.headers.get("Accept") == "application/json":
        # Resposta JSON para Postman/API
        return resposta_padrao(
            True,
            f"Animes listados com sucesso{f' (status: {status})' if status else ''}",
            dados={"animes": animes, "total": len(animes)}
        )
    
    # Resposta HTML (se tiver template)
    return jsonify(animes)


# =========================
# CRIAR
# =========================
@anime_bp.route("/animes", methods=["POST"])
@requer_autenticacao
@api_error_handler
def criar_anime():
    """
    Cria um novo anime para o usuário logado
    
    Body JSON:
    {
        "nome": "Nome do Anime",
        "descricao": "Descrição",
        "status": "assistindo|concluido|favorito",
        "eps_assistidos": 0,
        "total_eps": 12,
        "imagem": "url_da_imagem"
    }
    """
    usuario_id = session.get("id_usuario")
    
    dados = request.get_json()
    
    if not dados:
        raise ValueError("Nenhum dado fornecido. Envie JSON no body.")
    
    # Validações
    if not dados.get("nome"):
        raise ValueError("Campo 'nome' é obrigatório")
    
    # Adiciona usuario_id automaticamente
    dados["usuario_id"] = usuario_id
    
    AnimeService.criar(dados)
    
    return resposta_padrao(
        True,
        "Anime criado com sucesso!",
        codigo=201
    )


# =========================
# BUSCAR POR ID
# =========================
@anime_bp.route("/animes/<int:id>", methods=["GET"])
@requer_autenticacao
@api_error_handler
def buscar_anime(id):
    """
    Busca um anime específico por ID
    """
    anime = AnimeService.buscar_por_id(id)

    if not anime:
        return resposta_padrao(
            False,
            "Anime não encontrado",
            codigo=404
        )
    
    # Verifica se o anime pertence ao usuário
    usuario_id = session.get("id_usuario")
    if anime.get("usuario_id") != usuario_id:
        return resposta_padrao(
            False,
            "Você não tem permissão para acessar este anime",
            codigo=403
        )

    return resposta_padrao(
        True,
        "Anime encontrado",
        dados={"anime": anime}
    )


# =========================
# ATUALIZAR
# =========================
@anime_bp.route("/animes/<int:id>", methods=["PUT"])
@requer_autenticacao
@api_error_handler
def atualizar_anime(id):
    """
    Atualiza um anime existente
    
    Body JSON:
    {
        "nome": "Novo nome",
        "status": "concluido",
        "eps_assistidos": 12
    }
    """
    usuario_id = session.get("id_usuario")
    
    # Verifica se o anime existe e pertence ao usuário
    anime = AnimeService.buscar_por_id(id)
    
    if not anime:
        return resposta_padrao(
            False,
            "Anime não encontrado",
            codigo=404
        )
    
    if anime.get("usuario_id") != usuario_id:
        return resposta_padrao(
            False,
            "Você não tem permissão para editar este anime",
            codigo=403
        )
    
    dados = request.get_json()
    
    if not dados:
        raise ValueError("Nenhum dado fornecido para atualização")
    
    AnimeService.atualizar(id, dados)

    return resposta_padrao(
        True,
        "Anime atualizado com sucesso"
    )


# =========================
# DELETAR
# =========================
@anime_bp.route("/animes/<int:id>", methods=["DELETE"])
@requer_autenticacao
@api_error_handler
def deletar_anime(id):
    """
    Deleta um anime
    """
    usuario_id = session.get("id_usuario")
    
    # Verifica se o anime existe e pertence ao usuário
    anime = AnimeService.buscar_por_id(id)
    
    if not anime:
        return resposta_padrao(
            False,
            "Anime não encontrado",
            codigo=404
        )
    
    if anime.get("usuario_id") != usuario_id:
        return resposta_padrao(
            False,
            "Você não tem permissão para deletar este anime",
            codigo=403
        )
    
    AnimeService.deletar(id)
    
    return resposta_padrao(
        True,
        "Anime removido com sucesso"
    )


# =========================
# ROTAS ADICIONAIS ÚTEIS
# =========================

@anime_bp.route("/animes/estatisticas", methods=["GET"])
@requer_autenticacao
@api_error_handler
def estatisticas():
    """
    Retorna estatísticas dos animes do usuário
    """
    usuario_id = session.get("id_usuario")
    
    todos = AnimeService.listar(usuario_id)
    assistindo = AnimeService.listar(usuario_id, "assistindo")
    concluidos = AnimeService.listar(usuario_id, "concluido")
    favoritos = AnimeService.listar(usuario_id, "favorito")
    
    # Calcula total de episódios assistidos
    total_eps = sum(anime.get("eps_assistidos", 0) for anime in todos)
    
    stats = {
        "total_animes": len(todos),
        "assistindo": len(assistindo),
        "concluidos": len(concluidos),
        "favoritos": len(favoritos),
        "total_episodios_assistidos": total_eps
    }
    
    return resposta_padrao(
        True,
        "Estatísticas calculadas",
        dados={"estatisticas": stats}
    )


@anime_bp.route("/animes/<int:id>/proximo-episodio", methods=["POST"])
@requer_autenticacao
@api_error_handler
def proximo_episodio(id):
    """
    Incrementa o número de episódios assistidos
    """
    usuario_id = session.get("id_usuario")
    
    anime = AnimeService.buscar_por_id(id)
    
    if not anime:
        return resposta_padrao(False, "Anime não encontrado", codigo=404)
    
    if anime.get("usuario_id") != usuario_id:
        return resposta_padrao(False, "Acesso negado", codigo=403)
    
    eps_atual = anime.get("eps_assistidos", 0)
    total_eps = anime.get("total_eps", 0)
    
    if eps_atual >= total_eps:
        return resposta_padrao(
            False,
            "Você já assistiu todos os episódios!",
            codigo=400
        )
    
    # Atualiza
    dados_atualizacao = {
        "eps_assistidos": eps_atual + 1
    }
    
    # Se assistiu todos, muda status para concluído
    if eps_atual + 1 == total_eps:
        dados_atualizacao["status"] = "concluido"
    
    AnimeService.atualizar(id, dados_atualizacao)
    
    return resposta_padrao(
        True,
        f"Episódio {eps_atual + 1} marcado como assistido!" +
        (" Anime concluído! 🎉" if eps_atual + 1 == total_eps else ""),
        dados={
            "eps_assistidos": eps_atual + 1,
            "total_eps": total_eps,
            "concluido": eps_atual + 1 == total_eps
        }
    )