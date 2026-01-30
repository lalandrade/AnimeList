from db import get_connection

class UsuarioRepository:

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return usuarios

    @staticmethod
    def adicionar(usuario):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO usuarios (id, nome, cpf, email, idade, senha, perfil)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                usuario.id,
                usuario.nome,
                usuario.cpf,
                usuario.email,
                usuario.idade,
                usuario.senha,
                usuario.perfil
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao adicionar usuário:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        return usuario

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        deletado = cur.rowcount
        cur.close()
        conn.close()
        return deletado > 0

    @staticmethod
    def atualizar(usuario_edit):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE usuarios
                SET nome = %s,
                    email = %s,
                    idade = %s
                WHERE id = %s
            """, (
                usuario_edit["nome"],
                usuario_edit["email"],
                usuario_edit["idade"],
                usuario_edit["id"]
            ))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("Erro ao atualizar usuário:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
