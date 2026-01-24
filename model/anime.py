class Anime:
    def __init__(
        self,
        id,
        nome,
        descricao,
        status,
        total_eps,
        eps_assistidos,
        imagem,
        usuario_id
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.total_eps = total_eps
        self.eps_assistidos = eps_assistidos
        self.imagem = imagem
        self.usuario_id = usuario_id
