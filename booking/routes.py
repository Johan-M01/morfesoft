from datetime import datetime, timedelta, time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import and_
from extensions import db
from models import Business, Service, Availability, Appointment

booking_bp = Blueprint("booking", __name__, template_folder="../templates")

@booking_bp.get("/b/<slug>")
def business_public(slug):
    biz = Business.query.filter_by(slug=slug).first_or_404()
    services = Service.query.filter_by(business_id=biz.id).all()
    # fecha seleccionada (hoy por defecto)
    date_str = request.args.get("date")
    if date_str:
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        day = datetime.now().date()
    slots = compute_slots(biz, day)
    return render_template("public_booking.html", biz=biz, services=services, day=day, slots=slots)

@booking_bp.post("/b/<slug>/book")
def book(slug):
    biz = Business.query.filter_by(slug=slug).first_or_404()
    name = request.form.get("name")
    phone = request.form.get("phone")
    service_id = int(request.form.get("service_id"))
    start_at = datetime.fromisoformat(request.form.get("start_at"))
    service = Service.query.filter_by(id=service_id, business_id=biz.id).first_or_404()
    # bloquear solapes
    end_at = start_at + timedelta(minutes=service.duration_minutes)
    conflict = (Appointment.query.filter_by(business_id=biz.id)
                .filter(and_(Appointment.start_at < end_at, Appointment.start_at >= start_at - timedelta(minutes=service.duration_minutes))).first())
    if conflict:
        flash("Ese horario se ocupó, elige otro.", "danger")
        return redirect(url_for("booking.business_public", slug=biz.slug))
    appt = Appointment(business_id=biz.id, service_id=service.id,
                       customer_name=name, customer_phone=phone,
                       start_at=start_at, status="confirmed")
    db.session.add(appt)
    db.session.commit()
    flash("Reserva confirmada ✅", "success")
    return redirect(url_for("booking.business_public", slug=biz.slug))

def compute_slots(biz, day):
    from datetime import datetime, timedelta
    avails = Availability.query.filter_by(business_id=biz.id, day_of_week=day.weekday()).all()
    taken = {a.start_at for a in Appointment.query.filter_by(business_id=biz.id).all()
             if a.start_at.date() == day}
    slots = []
    for a in avails:
        cur = datetime.combine(day, a.start_time)
        end = datetime.combine(day, a.end_time)
        while cur < end:
            if cur not in taken:
                slots.append(cur)
            cur += timedelta(minutes=a.step_minutes)
    return slots
