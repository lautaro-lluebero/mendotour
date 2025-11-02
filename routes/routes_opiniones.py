from decorators import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import db
from models.opiniones import Opinion
from models.users import Users
from datetime import datetime

routes_opiniones = Blueprint('routes_opiniones', __name__, url_prefix='/opiniones')

# LISTAR + FORM abajo (usa templates/opiniones.html)
@routes_opiniones.route('/', methods=['GET'])
def index():
    rows = (
        db.session.query(Opinion, Users.username)
        .join(Users, Opinion.user_id == Users.id)
        .order_by(Opinion.created_at.desc())
        .all()
    )
    opiniones = [
        {"id": op.id, "contenido": op.contenido, "created_at": op.created_at, "username": username}
        for op, username in rows
    ]
    return render_template('opiniones.html', opiniones=opiniones)

# CREAR (solo logueados)
@routes_opiniones.route('/crear', methods=['POST'])
@login_required
def crear():
    contenido = (request.form.get('contenido') or '').strip()
    if not contenido:
        flash('Escribí tu opinión antes de enviar.', 'warning')
        return redirect(url_for('routes_opiniones.index'))

    op = Opinion(user_id=session.get('user_id'), contenido=contenido, created_at=datetime.utcnow())
    db.session.add(op)
    db.session.commit()
    flash('¡Gracias por tu opinión!', 'success')
    return redirect(url_for('routes_opiniones.index'))

# (Opcional) compatibilidad si alguna vez llamaste a .nueva
@routes_opiniones.route('/nueva', methods=['GET'])
def nueva():
    return redirect(url_for('routes_opiniones.index'))
