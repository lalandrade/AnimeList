import uuid
import bcrypt

class Usuario:
    def __init__(self, nome, cpf, email, idade, senha, perfil, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade
        self.senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.perfil = perfil


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "idade": self.idade,
            "senha": self.senha,
            "perfil": self.perfil
        }