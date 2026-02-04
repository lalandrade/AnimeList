from repository.anime_repository import AnimeRepository

class AnimeService:

    @staticmethod
    def listar(usuario_id, status=None):
        """
        Lista animes de um usuário, opcionalmente filtrados por status
        """
        try:
            if not usuario_id:
                raise ValueError("ID do usuário é obrigatório")
            
            animes = AnimeRepository.listar(usuario_id, status)
            
            # Converte para lista de dicts se necessário
            return [dict(anime) for anime in animes]
            
        except Exception as e:
            print(f"Erro ao listar animes: {e}")
            raise

    @staticmethod
    def criar(dados):
        """
        Cria um novo anime
        """
        try:
            # Validações
            if not dados.get("nome"):
                raise ValueError("Nome do anime é obrigatório")
            
            if not dados.get("usuario_id"):
                raise ValueError("ID do usuário é obrigatório")
            
            # Define valores padrão
            dados.setdefault("status", "assistindo")
            dados.setdefault("eps_assistidos", 0)
            dados.setdefault("total_eps", 0)
            dados.setdefault("descricao", "")
            dados.setdefault("imagem", "")
            
            # Validações adicionais
            if dados.get("eps_assistidos", 0) < 0:
                raise ValueError("Episódios assistidos não pode ser negativo")
            
            if dados.get("total_eps", 0) < 0:
                raise ValueError("Total de episódios não pode ser negativo")
            
            if dados.get("eps_assistidos", 0) > dados.get("total_eps", 0) and dados.get("total_eps", 0) > 0:
                raise ValueError("Episódios assistidos não pode ser maior que o total")
            
            status_validos = ["assistindo", "concluido", "favorito", "planejado", "pausado", "dropado"]
            if dados.get("status") not in status_validos:
                raise ValueError(f"Status inválido. Use: {', '.join(status_validos)}")
            
            AnimeRepository.adicionar(dados)
            return True
            
        except Exception as e:
            print(f"Erro ao criar anime: {e}")
            raise

    @staticmethod
    def buscar_por_id(id):
        """
        Busca um anime por ID
        """
        try:
            if not id:
                raise ValueError("ID é obrigatório")
            
            anime = AnimeRepository.buscar_por_id(id)
            
            if anime:
                return dict(anime)
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar anime: {e}")
            raise

    @staticmethod
    def atualizar(id, dados):
        """
        Atualiza um anime existente
        """
        try:
            if not id:
                raise ValueError("ID é obrigatório")
            
            if not dados:
                raise ValueError("Nenhum dado fornecido para atualização")
            
            # Busca anime atual para mesclar dados
            anime_atual = AnimeRepository.buscar_por_id(id)
            
            if not anime_atual:
                raise ValueError("Anime não encontrado")
            
            # Prepara dados para atualização (mantém valores atuais se não fornecidos)
            dados_completos = {
                "nome": dados.get("nome", anime_atual.get("nome")),
                "descricao": dados.get("descricao", anime_atual.get("descricao")),
                "status": dados.get("status", anime_atual.get("status")),
                "eps_assistidos": dados.get("eps_assistidos", anime_atual.get("eps_assistidos")),
                "total_eps": dados.get("total_eps", anime_atual.get("total_eps")),
                "imagem": dados.get("imagem", anime_atual.get("imagem"))
            }
            
            # Validações
            if dados_completos.get("eps_assistidos", 0) < 0:
                raise ValueError("Episódios assistidos não pode ser negativo")
            
            if dados_completos.get("total_eps", 0) < 0:
                raise ValueError("Total de episódios não pode ser negativo")
            
            if (dados_completos.get("eps_assistidos", 0) > dados_completos.get("total_eps", 0) 
                and dados_completos.get("total_eps", 0) > 0):
                raise ValueError("Episódios assistidos não pode ser maior que o total")
            
            status_validos = ["assistindo", "concluido", "favorito", "planejado", "pausado", "dropado"]
            if dados_completos.get("status") not in status_validos:
                raise ValueError(f"Status inválido. Use: {', '.join(status_validos)}")
            
            AnimeRepository.atualizar(id, dados_completos)
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar anime: {e}")
            raise

    @staticmethod
    def deletar(id):
        """
        Deleta um anime
        """
        try:
            if not id:
                raise ValueError("ID é obrigatório")
            
            # Verifica se existe
            anime = AnimeRepository.buscar_por_id(id)
            
            if not anime:
                raise ValueError("Anime não encontrado")
            
            AnimeRepository.deletar(id)
            return True
            
        except Exception as e:
            print(f"Erro ao deletar anime: {e}")
            raise

    @staticmethod
    def listar_por_status(usuario_id, status):
        """
        Atalho para listar por status específico
        """
        return AnimeService.listar(usuario_id, status)

    @staticmethod
    def contar_por_status(usuario_id):
        """
        Retorna contagem de animes por status
        """
        try:
            todos = AnimeRepository.listar(usuario_id)
            
            contagem = {
                "assistindo": 0,
                "concluido": 0,
                "favorito": 0,
                "planejado": 0,
                "pausado": 0,
                "dropado": 0,
                "total": len(todos)
            }
            
            for anime in todos:
                status = anime.get("status", "assistindo")
                if status in contagem:
                    contagem[status] += 1
            
            return contagem
            
        except Exception as e:
            print(f"Erro ao contar animes: {e}")
            raise