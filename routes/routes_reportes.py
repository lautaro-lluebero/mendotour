from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.db import db
from models.reportes import Reportes

routes_reportes = Blueprint('routes_reportes', __name__, url_prefix='/reportes')

def is_logged_in():
    return bool(session.get('logged_in'))

def is_admin():
    return (session.get('rol', '') or '').lower() == 'administrador'

@routes_reportes.route('/', methods=['GET', 'POST'])
def generar_reporte():
    # Debe estar logueado para entrar aquí
    if not is_logged_in():
        flash("Tenés que iniciar sesión para generar un reporte", "warning")
        return redirect(url_for('routes_auth.login'))

    if request.method == 'POST':
        # Cualquiera logueado puede generar
        user_id = session.get('user_id')
        tipo = (request.form.get('tipo') or 'Reporte general').strip()

        nuevo = Reportes(user_id=user_id, tipo=tipo)
        db.session.add(nuevo)
        db.session.commit()

        flash("Reporte generado y guardado correctamente", "success")
        return redirect(url_for('routes_reportes.generar_reporte'))

    # GET: solo administradores ven el historial
    historial = Reportes.query.order_by(Reportes.fecha.desc()).all() if is_admin() else None

    return render_template(
        'reportes.html',
        historial=historial,   # tu template espera este nombre
    )
