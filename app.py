from flask import Flask
from controller.usuario_controller import usuario_bp

app = Flask(__name__)

# CHAVE DE SESSÃO (obrigatório)
app.secret_key = "anime_list_secret_key"

# REGISTRAR O BLUEPRINT
app.register_blueprint(usuario_bp)

if __name__ == "__main__":
    app.run(debug=True)
