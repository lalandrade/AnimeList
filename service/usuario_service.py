import uuid
import bcrypt
from repository.usuario_repository import UsuarioRepository
from model.usuario import Usuario

class UsuarioService:

    @staticmethod
    def cadastrar(dados):
        # 🔥 GERA UUID
        dados["id"] = str(uuid.uuid4())

        # 🔐 hash da senha
        senha_hash = bcrypt.hashpw(
            dados["senha"].encode("utf-8"),
            bcrypt.gensalt()
        )
        dados["senha"] = senha_hash.decode("utf-8")

        usuario = Usuario(**dados)
        return UsuarioRepository.adicionar(usuario)

    @staticmethod
    def autenticar(email, senha):
        usuario = UsuarioRepository.buscar_por_email(email)
        if usuario and bcrypt.checkpw(
            senha.encode("utf-8"),
            usuario["senha"].encode("utf-8")
        ):
            return usuario
        return None

    @staticmethod
    def atualizar(usuario_edit):
        dados_permitidos = {k: v for k, v in usuario_edit.items() if v is not None}
        return UsuarioRepository.atualizar(dados_permitidos)

    @staticmethod
    def deletar(id):
        return UsuarioRepository.deletar(id)

    @staticmethod
    def listar():
        return UsuarioRepository.listar()
