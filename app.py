from flask import Flask
from controller.usuario_controller import usuario_bp
from controller.anime_controller import anime_bp

app = Flask(__name__)

app.secret_key = "anime_list_secret_key"

app.register_blueprint(usuario_bp)
app.register_blueprint(anime_bp)

if __name__ == "__main__":
    app.run(debug=True)
