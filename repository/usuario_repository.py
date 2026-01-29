from db import get_connection
from psycopg2.extras import RealDictCursor

class UsuarioRepository:

    @staticmethod
    def adicionar(dados):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO usuarios (id, nome, cpf, email, idade, senha, perfil)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["id"],
                dados["nome"],
                dados["cpf"],
                dados["email"],
                dados["idade"],
                dados["senha"],
                dados["perfil"]
            ))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Erro ao adicionar usuário:", e)
            return False

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()

        cur.close()
        conn.close()
        return usuario

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT id, nome, email, idade, perfil FROM usuarios")
        usuarios = cur.fetchall()

        cur.close()
        conn.close()
        return usuarios

    @staticmethod
    def atualizar(dados):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE usuarios
            SET nome = %s, email = %s, idade = %s, perfil = %s
            WHERE id = %s
        """, (
            dados["nome"],
            dados["email"],
            dados["idade"],
            dados["perfil"],
            dados["id"]
        ))

        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        deletado = cur.rowcount > 0

        conn.commit()
        cur.close()
        conn.close()
        return deletado
