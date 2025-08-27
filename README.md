\# 🚀 MorfeSoft



\*\*MorfeSoft\*\* es un portal de reservas y gestión de servicios, construido con \*\*Flask + Bootstrap 5\*\*.  

Permite a negocios crear su panel, definir servicios, horarios y compartir su link público para que los clientes reserven en línea.



---



\## ✨ Características principales

\- 🔑 Registro / login de usuarios

\- 🛠️ Configuración de servicios (con duración y depósito opcional)

\- ⏰ Disponibilidad semanal por día y franja horaria

\- 📅 Gestión de citas (clientes reservan desde una página pública)

\- 🌙 Interfaz dark moderna (Bootstrap 5 + diseño custom)

\- ⚡ Listo para integración futura de pagos (Stripe / PayPal)

\- 📩 Soporte opcional de notificaciones por correo vía SMTP



---



\## 📸 Screenshots

\### Dashboard

!\[Dashboard](docs/screenshots/dashboard.png)



\### Disponibilidad

!\[Disponibilidad](docs/screenshots/disponibilidad.png)



\### Citas

!\[Citas](docs/screenshots/citas.png)



---



\## 🛠️ Instalación local



```bash

\# 1) Clona el repo

git clone https://github.com/Johan-M01/morfesoft.git

cd morfesoft



\# 2) Crea entorno virtual

python -m venv .venv

.venv\\Scripts\\activate   # en Windows



\# 3) Instala dependencias

pip install -r requirements.txt



\# 4) Inicializa la DB

python init\_db.py



\# 5) Ejecuta

python app.py



