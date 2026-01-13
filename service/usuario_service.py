from model.usuario import Usuario
from repository.usuario_repository import UsuarioRepository
import bcrypt

class UsuarioService:

    @staticmethod
    def cadastrar(dados):
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
        dados_permitidos = {
        "id": usuario_edit.get("id"),
        "nome": usuario_edit.get("nome"),
        "email": usuario_edit.get("email"),
        "idade": usuario_edit.get("idade")
    }
        return UsuarioRepository.atualizar(dados_permitidos)


    
    @staticmethod
    def deletar(id):
        
        return UsuarioRepository.deletar(id)

    @staticmethod
    def listar():
        return UsuarioRepository.listar()
