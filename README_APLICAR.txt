# MorfeSoft Functional Patch
Archivos que añaden:
- Modelos: Business, Service, Availability, Appointment
- Blueprints: /dashboard (services, availability, appointments, account POST), /booking (página pública)
- Plantillas Bootstrap 5 para CRUD y reservas

## Cómo aplicar
1. Copia los contenidos de `models_patch/models.py.append` **al final** de tu `models.py` existente (reemplazando el User que tengas si hace falta). O sustituye `models.py` por uno combinado.
2. Reemplaza `dashboard/routes.py` por el incluido en este patch.
3. Añade el blueprint público: copiar carpeta `booking/` a tu proyecto.
4. En `app.py`, registra el blueprint público:
   ```python
   from booking.routes import booking_bp
   app.register_blueprint(booking_bp, url_prefix="/booking")
   ```
5. Reemplaza plantillas en `templates/` por las de este patch (o copia las nuevas que no existan).
6. Vuelve a crear tablas si hace falta:
   ```powershell
   python init_db.py
   ```
