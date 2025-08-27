from datetime import datetime, time
from flask_login import UserMixin
from extensions import db

# ------------------------
# Usuarios
# ------------------------
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(150), nullable=False)

    # Relación 1–1 con su negocio
    business = db.relationship("Business", back_populates="owner", uselist=False)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

# ------------------------
# Negocio (perfil público)
# ------------------------
class Business(db.Model):
    __tablename__ = "business"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False, default="Mi negocio")
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)

    owner = db.relationship("User", back_populates="business")
    services = db.relationship("Service", back_populates="business",
                               cascade="all, delete-orphan")
    availability = db.relationship("Availability", back_populates="business",
                                   cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", back_populates="business",
                                   cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Business {self.slug}>"

# ------------------------
# Servicios
# ------------------------
class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    deposit_cents = db.Column(db.Integer)  # opcional (None = sin depósito)

    business = db.relationship("Business", back_populates="services")
    appointments = db.relationship("Appointment", back_populates="service")

    def __repr__(self) -> str:
        return f"<Service {self.name} ({self.duration_minutes}m)>"

# ------------------------
# Disponibilidad semanal
# ------------------------
class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Lun … 6=Dom
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    step_minutes = db.Column(db.Integer, nullable=False, default=30)

    business = db.relationship("Business", back_populates="availability")

    def __repr__(self) -> str:
        return f"<Avail d={self.day_of_week} {self.start_time}-{self.end_time}>"

# ------------------------
# Citas
# ------------------------
class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(60))
    start_at = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="confirmed")  # confirmed/cancelled/no-show

    business = db.relationship("Business", back_populates="appointments")
    service = db.relationship("Service", back_populates="appointments")

    def __repr__(self) -> str:
        return f"<Appt {self.customer_name} {self.start_at:%Y-%m-%d %H:%M}>"
