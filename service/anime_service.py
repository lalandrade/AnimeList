from repository.anime_repository import AnimeRepository

class AnimeService:

    @staticmethod
    def listar(usuario_id, status=None):
        return AnimeRepository.listar(usuario_id, status)

    @staticmethod
    def criar(dados):
        AnimeRepository.adicionar(dados)

    @staticmethod
    def buscar_por_id(id):
        return AnimeRepository.buscar_por_id(id)

    @staticmethod
    def atualizar(id, dados):
        AnimeRepository.atualizar(id, dados)

    @staticmethod
    def deletar(id):
        AnimeRepository.deletar(id)
