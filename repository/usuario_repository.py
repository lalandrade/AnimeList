from db import get_connection

class UsuarioRepository:

    @staticmethod
    def listar():
        """
        Lista todos os usuários
        Retorna lista vazia em caso de erro
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios")
            usuarios = cur.fetchall()
            return usuarios if usuarios else []
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def adicionar(usuario):
        """
        Adiciona um novo usuário
        Retorna True se sucesso, False se erro
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Garante que a senha está como string UTF-8
            senha_valor = usuario.senha
            if isinstance(senha_valor, bytes):
                senha_valor = senha_valor.decode('utf-8')
            
            cur.execute("""
                INSERT INTO usuarios (id, nome, cpf, email, idade, senha, perfil)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                usuario.id,
                usuario.nome,
                usuario.cpf,
                usuario.email,
                usuario.idade,
                senha_valor,  # Usa a senha convertida
                usuario.perfil
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_email(email):
        """
        Busca usuário por email
        Retorna None se não encontrado
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cur.fetchone()
            
            # Converte RealDictRow para dict normal se necessário
            if usuario:
                usuario_dict = dict(usuario)
                # Garante que senha está como string
                if "senha" in usuario_dict and isinstance(usuario_dict["senha"], bytes):
                    usuario_dict["senha"] = usuario_dict["senha"].decode('utf-8')
                return usuario_dict
            
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(id):
        """
        Busca usuário por ID
        Retorna None se não encontrado
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            usuario = cur.fetchone()
            
            # Converte para dict e garante encoding
            if usuario:
                usuario_dict = dict(usuario)
                if "senha" in usuario_dict and isinstance(usuario_dict["senha"], bytes):
                    usuario_dict["senha"] = usuario_dict["senha"].decode('utf-8')
                return usuario_dict
            
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def deletar(id):
        """
        Deleta um usuário
        Retorna True se deletado, False se não encontrado
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            conn.commit()
            deletado = cur.rowcount > 0
            return deletado
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def atualizar(usuario_edit):
        """
        Atualiza dados de um usuário
        Retorna True se atualizado, False se não encontrado
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Constrói query dinâmica baseada nos campos fornecidos
            campos_atualizar = []
            valores = []
            
            if "nome" in usuario_edit:
                campos_atualizar.append("nome = %s")
                valores.append(usuario_edit["nome"])
            
            if "email" in usuario_edit:
                campos_atualizar.append("email = %s")
                valores.append(usuario_edit["email"])
            
            if "idade" in usuario_edit:
                campos_atualizar.append("idade = %s")
                valores.append(usuario_edit["idade"])
            
            if "cpf" in usuario_edit:
                campos_atualizar.append("cpf = %s")
                valores.append(usuario_edit["cpf"])
            
            if "perfil" in usuario_edit:
                campos_atualizar.append("perfil = %s")
                valores.append(usuario_edit["perfil"])
            
            # Se não há campos para atualizar, retorna False
            if not campos_atualizar:
                return False
            
            # Adiciona o ID no final
            valores.append(usuario_edit["id"])
            
            # Monta e executa a query
            query = f"UPDATE usuarios SET {', '.join(campos_atualizar)} WHERE id = %s"
            cur.execute(query, valores)
            conn.commit()
            
            return cur.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def email_existe(email, excluir_id=None):
        """
        Verifica se email já existe no banco
        Útil para validação antes de cadastrar/atualizar
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            if excluir_id:
                cur.execute(
                    "SELECT COUNT(*) FROM usuarios WHERE email = %s AND id != %s",
                    (email, excluir_id)
                )
            else:
                cur.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))
            
            count = cur.fetchone()[0]
            return count > 0
            
        except Exception as e:
            print(f"Erro ao verificar email: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def cpf_existe(cpf, excluir_id=None):
        """
        Verifica se CPF já existe no banco
        Útil para validação antes de cadastrar/atualizar
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            if excluir_id:
                cur.execute(
                    "SELECT COUNT(*) FROM usuarios WHERE cpf = %s AND id != %s",
                    (cpf, excluir_id)
                )
            else:
                cur.execute("SELECT COUNT(*) FROM usuarios WHERE cpf = %s", (cpf,))
            
            count = cur.fetchone()[0]
            return count > 0
            
        except Exception as e:
            print(f"Erro ao verificar CPF: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()