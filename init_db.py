from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print("✅ Base de datos creada correctamente (db.sqlite3).")
