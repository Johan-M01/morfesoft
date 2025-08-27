from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from extensions import db, migrate, login_manager
from auth.routes import auth_bp
from dashboard.routes import dashboard_bp
from booking.routes import booking_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(booking_bp, url_prefix="/booking")

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.dashboard"))
        # si no estás logueado, intenta servir index.html
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
