from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instancias de extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# A dónde enviar cuando se requiere login
login_manager.login_view = "auth.login"

# Cargador de usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id: str):
    # Importación diferida para evitar import circular
    from models import User
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None
