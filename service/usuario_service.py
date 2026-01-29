import bcrypt
import uuid
from repository.usuario_repository import UsuarioRepository

class UsuarioService:

    @staticmethod
    def cadastrar(dados):
        try:
            dados["id"] = str(uuid.uuid4())

            senha_hash = bcrypt.hashpw(
                dados["senha"].encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            dados["senha"] = senha_hash

            return UsuarioRepository.adicionar(dados)

        except Exception as e:
            print("Erro no service:", e)
            return False

    @staticmethod
    def autenticar(email, senha):
        usuario = UsuarioRepository.buscar_por_email(email)
        if not usuario:
            return None

        if bcrypt.checkpw(
            senha.encode("utf-8"),
            usuario["senha"].encode("utf-8")
        ):
            return usuario

        return None

    @staticmethod
    def listar():
        return UsuarioRepository.listar()

    @staticmethod
    def atualizar(dados):
        return UsuarioRepository.atualizar(dados)

    @staticmethod
    def deletar(id):
        return UsuarioRepository.deletar(id)
