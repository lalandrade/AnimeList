import uuid
import bcrypt
from repository.usuario_repository import UsuarioRepository
from model.usuario import Usuario

class UsuarioService:

    @staticmethod
    def cadastrar(dados):
        """
        Cadastra um novo usuário
        Lança exceções específicas para erros conhecidos
        """
        try:
            # 🔥 GERA UUID
            dados["id"] = str(uuid.uuid4())

            # 🔐 hash da senha - FIX ENCODING
            senha_str = str(dados["senha"])  # Garante que é string
            senha_hash = bcrypt.hashpw(
                senha_str.encode("utf-8"),
                bcrypt.gensalt()
            )
            dados["senha"] = senha_hash.decode("utf-8")

            usuario = Usuario(**dados)
            resultado = UsuarioRepository.adicionar(usuario)
            
            if not resultado:
                raise ValueError("Falha ao salvar usuário no banco de dados")
            
            return resultado
            
        except KeyError as e:
            raise ValueError(f"Campo obrigatório ausente: {str(e)}")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            raise

    @staticmethod
    def autenticar(email, senha):
        """
        Autentica um usuário
        Retorna dados do usuário ou None
        """
        try:
            if not email or not senha:
                return None
                
            usuario = UsuarioRepository.buscar_por_email(email)
            
            if not usuario:
                return None
            
            # FIX: Garante encoding correto
            senha_str = str(senha)
            senha_hash_db = usuario["senha"]
            
            # Se a senha do banco vier como string, garante encoding UTF-8
            if isinstance(senha_hash_db, str):
                senha_hash_bytes = senha_hash_db.encode("utf-8")
            else:
                senha_hash_bytes = senha_hash_db
            
            # Verifica senha
            senha_valida = bcrypt.checkpw(
                senha_str.encode("utf-8"),
                senha_hash_bytes
            )
            
            if senha_valida:
                return usuario
            
            return None
            
        except UnicodeDecodeError as e:
            print(f"Erro de encoding na autenticação: {e}")
            print(f"Tipo senha DB: {type(usuario.get('senha'))}")
            return None
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def atualizar(usuario_edit):
        """
        Atualiza dados de um usuário
        Lança exceção se falhar
        """
        try:
            if not usuario_edit.get("id"):
                raise ValueError("ID do usuário é obrigatório para atualização")
            
            dados_permitidos = {k: v for k, v in usuario_edit.items() if v is not None}
            resultado = UsuarioRepository.atualizar(dados_permitidos)
            
            if not resultado:
                raise ValueError("Usuário não encontrado ou nenhuma alteração realizada")
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            raise

    @staticmethod
    def deletar(id):
        """
        Deleta um usuário
        """
        try:
            if not id:
                raise ValueError("ID do usuário é obrigatório")
            
            return UsuarioRepository.deletar(id)
            
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            raise

    @staticmethod
    def listar():
        """
        Lista todos os usuários
        """
        try:
            usuarios = UsuarioRepository.listar()
            
            # Remove senhas antes de retornar (segurança)
            usuarios_sem_senha = []
            for usuario in usuarios:
                usuario_dict = dict(usuario)  # Converte para dict se necessário
                if "senha" in usuario_dict:
                    del usuario_dict["senha"]
                usuarios_sem_senha.append(usuario_dict)
            
            return usuarios_sem_senha
            
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            raise

    @staticmethod
    def buscar_por_id(id):
        """
        Busca um usuário específico por ID
        """
        try:
            if not id:
                raise ValueError("ID do usuário é obrigatório")
            
            usuario = UsuarioRepository.buscar_por_id(id)
            
            if usuario:
                usuario_dict = dict(usuario)
                if "senha" in usuario_dict:
                    del usuario_dict["senha"]  # Remove senha por segurança
                return usuario_dict
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            raise