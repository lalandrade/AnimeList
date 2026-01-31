import os
from flask import Flask
from controller.usuario_controller import usuario_bp
from controller.anime_controller import anime_bp
from dotenv import load_dotenv

# só carrega .env local
if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


app.register_blueprint(usuario_bp)
app.register_blueprint(anime_bp)

if __name__ == "__main__":
    app.run()
