from datetime import datetime, date, time, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Business, Service, Availability, Appointment

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates")

# -----------------------------
# Helpers
# -----------------------------
def _slugify(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace(" ", "-")
    # limpia caracteres poco seguros para URL
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-_"
    return "".join(ch for ch in s if ch in allowed) or "mi-negocio"

def _ensure_business() -> Business:
    """Crea un negocio por defecto si el usuario no lo tiene."""
    if not current_user.business:
        biz = Business(user_id=current_user.id, name="Mi negocio", slug=f"biz-{current_user.id}")
        db.session.add(biz)
        db.session.commit()
    return current_user.business

# -----------------------------
# Dashboard
# -----------------------------
@dashboard_bp.route("/")
@login_required
def dashboard():
    biz = _ensure_business()
    last_appts = (
        Appointment.query
        .filter_by(business_id=biz.id)
        .order_by(Appointment.start_at.desc())
        .limit(5)
        .all()
    )
    return render_template("dashboard.html", user=current_user, biz=biz, last_appts=last_appts)

# -----------------------------
# Cuenta (editar nombre y slug)
# -----------------------------
@dashboard_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    biz = _ensure_business()
    if request.method == "POST":
        name = request.form.get("name") or "Mi negocio"
        slug = _slugify(request.form.get("slug") or biz.slug)

        # validar slug único (que no sea de otro negocio)
        exists = Business.query.filter(
            Business.slug == slug,
            Business.id != biz.id
        ).first()
        if exists:
            flash("Ese slug ya está en uso. Prueba con otro.", "danger")
        else:
            biz.name = name
            biz.slug = slug
            db.session.commit()
            flash("Cuenta actualizada.", "success")
            return redirect(url_for("dashboard.account"))

    return render_template("account.html", user=current_user, biz=biz)

# -----------------------------
# Servicios (listar + crear + eliminar)
# -----------------------------
@dashboard_bp.route("/services", methods=["GET", "POST"])
@login_required
def services():
    biz = _ensure_business()

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        duration = int(request.form.get("duration") or 30)
        deposit_raw = request.form.get("deposit")
        deposit_cents = int(deposit_raw) if (deposit_raw and deposit_raw.isdigit()) else None

        if not name:
            flash("El nombre del servicio es obligatorio.", "danger")
        else:
            db.session.add(Service(
                business_id=biz.id,
                name=name,
                duration_minutes=max(5, duration),
                deposit_cents=deposit_cents
            ))
            db.session.commit()
            flash("Servicio creado.", "success")
            return redirect(url_for("dashboard.services"))

    items = Service.query.filter_by(business_id=biz.id).all()
    return render_template("services.html", biz=biz, items=items)

@dashboard_bp.post("/services/<int:sid>/delete")
@login_required
def services_delete(sid: int):
    biz = _ensure_business()
    s = Service.query.filter_by(id=sid, business_id=biz.id).first_or_404()
    db.session.delete(s)
    db.session.commit()
    flash("Servicio eliminado.", "success")
    return redirect(url_for("dashboard.services"))

# -----------------------------
# Disponibilidad (listar + crear + eliminar)
# -----------------------------
@dashboard_bp.route("/availability", methods=["GET", "POST"])
@login_required
def availability():
    biz = _ensure_business()

    if request.method == "POST":
        try:
            day = int(request.form.get("day"))
            start = request.form.get("start")
            end = request.form.get("end")
            step = int(request.form.get("step") or 30)

            s_hour, s_min = map(int, start.split(":"))
            e_hour, e_min = map(int, end.split(":"))

            if (e_hour, e_min) <= (s_hour, s_min):
                raise ValueError("El fin debe ser mayor al inicio.")

            db.session.add(Availability(
                business_id=biz.id,
                day_of_week=day,
                start_time=time(s_hour, s_min),
                end_time=time(e_hour, e_min),
                step_minutes=max(5, step),
            ))
            db.session.commit()
            flash("Disponibilidad agregada.", "success")
            return redirect(url_for("dashboard.availability"))
        except Exception as e:
            flash(f"Error al guardar disponibilidad: {e}", "danger")

    items = Availability.query.filter_by(business_id=biz.id).order_by(Availability.day_of_week).all()
    return render_template("availability.html", biz=biz, items=items)

@dashboard_bp.post("/availability/<int:aid>/delete")
@login_required
def availability_delete(aid: int):
    biz = _ensure_business()
    a = Availability.query.filter_by(id=aid, business_id=biz.id).first_or_404()
    db.session.delete(a)
    db.session.commit()
    flash("Disponibilidad eliminada.", "success")
    return redirect(url_for("dashboard.availability"))

# -----------------------------
# Citas (listar)
# -----------------------------
@dashboard_bp.route("/appointments")
@login_required
def appointments():
    biz = _ensure_business()
    items = (
        Appointment.query
        .filter_by(business_id=biz.id)
        .order_by(Appointment.start_at.desc())
        .all()
    )
    return render_template("appointments.html", biz=biz, items=items)
