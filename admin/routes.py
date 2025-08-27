from flask import Blueprint, render_template
from models import User, Business, Appointment
from extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    users = User.query.all()
    businesses = Business.query.all()
    appointments = Appointment.query.all()
    return render_template('admin/index.html', users=users, businesses=businesses, appointments=appointments)
