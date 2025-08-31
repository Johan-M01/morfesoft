# init_db.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno locales (.env)
load_dotenv()

from app import create_app
from extensions import db
from models import User, Business, Service, Availability, Appointment  # asegúrate de que existan

def _normalize_db_uri(uri: str) -> str:
    """Render entrega 'postgres://', pero SQLAlchemy necesita 'postgresql+psycopg2://'."""
    if uri and uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql+psycopg2://", 1)
    return uri

def main():
    app = create_app()

    # Intentar usar Postgres (Render) o fallback a SQLite
    env_uri = os.getenv("SQLALCHEMY_DATABASE_URI", "").strip()
    if env_uri:
        env_uri = _normalize_db_uri(env_uri)
        app.config["SQLALCHEMY_DATABASE_URI"] = env_uri
    else:
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite3")

    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente.")
        print(f"🔗 Usando: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == "__main__":
    main()
