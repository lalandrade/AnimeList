from db import get_connection

class AnimeRepository:

    @staticmethod
    def listar(usuario_id, status=None):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        if status:
            cur.execute("""
                SELECT * FROM animes
                WHERE usuario_id=%s AND status=%s
                ORDER BY id DESC
            """, (usuario_id, status))
        else:
            cur.execute("""
                SELECT * FROM animes
                WHERE usuario_id=%s
                ORDER BY id DESC
            """, (usuario_id,))

        data = cur.fetchall()
        conn.close()
        return data

    @staticmethod
    def adicionar(dados):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO animes
            (usuario_id, nome, descricao, status, eps_assistidos, total_eps, imagem)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            dados.get("usuario_id"),
            dados.get("nome"),
            dados.get("descricao"),
            dados.get("status", "assistindo"),
            dados.get("eps_assistidos", 0),
            dados.get("total_eps", 0),
            dados.get("imagem")
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM animes WHERE id=%s", (id,))
        data = cur.fetchone()
        conn.close()
        return data

    @staticmethod
    def atualizar(id, dados):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE animes SET
                nome=%s,
                descricao=%s,
                status=%s,
                eps_assistidos=%s,
                total_eps=%s,
                imagem=%s
            WHERE id=%s
        """, (
            dados.get("nome"),
            dados.get("descricao"),
            dados.get("status", "assistindo"),
            dados.get("eps_assistidos", 0),
            dados.get("total_eps", 0),
            dados.get("imagem"),
            id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM animes WHERE id=%s", (id,))
        conn.commit()
        conn.close()
