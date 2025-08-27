from models import Appointment
from sqlalchemy import func
from extensions import db

def get_stats():
    total_appointments = db.session.query(func.count(Appointment.id)).scalar()
    return {"total_appointments": total_appointments}
