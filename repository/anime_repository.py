from db import get_connection
from psycopg2.extras import RealDictCursor


class AnimeRepository:

    @staticmethod
    def listar(usuario_id, status=None):
        """
        Lista animes de um usuário, opcionalmente filtrados por status
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            if status:
                cur.execute("""
                    SELECT * FROM animes
                    WHERE usuario_id = %s AND status = %s
                    ORDER BY id DESC
                """, (usuario_id, status))
            else:
                cur.execute("""
                    SELECT * FROM animes
                    WHERE usuario_id = %s
                    ORDER BY id DESC
                """, (usuario_id,))

            data = cur.fetchall()
            return data if data else []
            
        except Exception as e:
            print(f"Erro ao listar animes: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def adicionar(dados):
        """
        Adiciona um novo anime ao banco
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO animes
                (usuario_id, nome, descricao, status, eps_assistidos, total_eps, imagem)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                dados.get("usuario_id"),
                dados.get("nome"),
                dados.get("descricao", ""),
                dados.get("status", "assistindo"),
                dados.get("eps_assistidos", 0),
                dados.get("total_eps", 0),
                dados.get("imagem", "")
            ))

            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar anime: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(id):
        """
        Busca um anime específico por ID
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("SELECT * FROM animes WHERE id = %s", (id,))
            data = cur.fetchone()

            return data
            
        except Exception as e:
            print(f"Erro ao buscar anime por ID: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def atualizar(id, dados):
        """
        Atualiza um anime existente
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                UPDATE animes SET
                    nome = %s,
                    descricao = %s,
                    status = %s,
                    eps_assistidos = %s,
                    total_eps = %s,
                    imagem = %s
                WHERE id = %s
            """, (
                dados.get("nome"),
                dados.get("descricao", ""),
                dados.get("status", "assistindo"),
                dados.get("eps_assistidos", 0),
                dados.get("total_eps", 0),
                dados.get("imagem", ""),
                id
            ))

            conn.commit()
            return cur.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao atualizar anime: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def deletar(id):
        """
        Deleta um anime
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("DELETE FROM animes WHERE id = %s", (id,))
            conn.commit()
            
            return cur.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao deletar anime: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_usuario(usuario_id):
        """
        Busca todos os animes de um usuário (alias para listar)
        """
        return AnimeRepository.listar(usuario_id)

    @staticmethod
    def contar_por_usuario(usuario_id):
        """
        Conta quantos animes um usuário tem
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM animes WHERE usuario_id = %s", (usuario_id,))
            count = cur.fetchone()[0]

            return count
            
        except Exception as e:
            print(f"Erro ao contar animes: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_nome(usuario_id, nome):
        """
        Busca animes por nome (busca parcial)
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("""
                SELECT * FROM animes
                WHERE usuario_id = %s AND LOWER(nome) LIKE LOWER(%s)
                ORDER BY id DESC
            """, (usuario_id, f"%{nome}%"))

            data = cur.fetchall()
            return data if data else []
            
        except Exception as e:
            print(f"Erro ao buscar anime por nome: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()