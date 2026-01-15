from db import get_connection

class AnimeRepository:

    @staticmethod
    def listar(usuario_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM animes WHERE usuario_id=%s ORDER BY id DESC",
            (usuario_id,)
        )
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
            dados["usuario_id"],
            dados["nome"],
            dados["descricao"],
            dados["status"],
            dados["eps_assistidos"],
            dados["total_eps"],
            dados["imagem"]
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
            dados["nome"],
            dados["descricao"],
            dados["status"],
            dados["eps_assistidos"],
            dados["total_eps"],
            dados["imagem"],
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
