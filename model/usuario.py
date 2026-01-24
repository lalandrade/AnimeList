import uuid
import bcrypt

class Usuario:
    def __init__(self, id, nome, cpf, email, idade, senha, perfil="user"):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade
        self.senha = senha  # ❗ NÃO faz hash aqui
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