import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="crud_db"
    )


class UsuarioRepository:

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios

    @staticmethod
    def adicionar(usuario):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
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
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        return deleted > 0

    @staticmethod
    def atualizar(usuario_edit):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
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
            return cursor.rowcount > 0
        except Exception as e:
            print("Erro ao atualizar usuário:", e)
            return False
        finally:
            cursor.close()
            conn.close()
