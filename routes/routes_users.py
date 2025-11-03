from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.users import Users
import re
from decorators import login_required, admin_required, owner_or_admin

routes_users = Blueprint('routes_users', __name__, url_prefix='/users')

# ---------- Helpers de validación ----------
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email))

def not_empty(*vals) -> bool:
    return all(v and str(v).strip() for v in vals)

# Lista blanca de roles aceptados
ALLOWED_ROLES = {"admin", "administrador", "user", "cliente", "editor"}

def normalize_role(rol: str) -> str:
    """Normaliza variantes comunes para que sean consistentes."""
    if not rol:
        return "cliente"
    return rol.strip().lower()

# ---------- CRUD ----------

# LISTAR (Panel)
# Admin ve todos; no-admin ve solo su propio registro
@routes_users.route('/', methods=['GET'])
@login_required
def get_users():
    is_admin = (session.get('rol') or '').lower() in {'admin', 'administrador'}
    if is_admin:
        users = Users.query.order_by(Users.id.asc()).all()
    else:
        me_id = session.get('user_id')
        users = Users.query.filter_by(id=me_id).all()
    return render_template('users/users.html', users=users, is_admin=is_admin)

# CREAR 
@routes_users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1) Tomar datos del form
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        rol      = normalize_role(request.form.get('rol', 'cliente'))

        # Validaciones
        if not not_empty(username, email, password):
            return render_template('users/register.html', error="Todos los campos son obligatorios")
        if not is_valid_email(email):
            return render_template('users/register.html', error="Email inválido")
        if rol not in ALLOWED_ROLES:
            return render_template('users/register.html', error=f"Rol inválido: {rol}")

        # Duplicados por email o username
        existing = Users.query.filter(or_(Users.email == email, Users.username == username)).first()
        if existing:
            msg = "Ese email ya está registrado" if existing.email == email else "Ese usuario ya existe"
            return render_template('users/register.html', error=msg)

        # Crear usuario
        new_user = Users(username=username, email=email, password=password, rol=rol)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('users/register.html', error="Usuario o email ya existe")

        flash(f"Usuario creado como {rol}", "success")
        return redirect(url_for('routes_users.get_users'))

    return render_template('users/register.html')

# EDITAR (form) — dueño o admin
@routes_users.route('/update/<int:id>', methods=['GET'])
@login_required
@owner_or_admin
def edit_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('home'))
    return render_template('users/edit_user.html', user=user)

# EDITAR (guardar) — dueño o admin
@routes_users.route('/update/<int:id>', methods=['POST'])
@login_required
@owner_or_admin
def update_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('home'))

    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')  # puede venir vacío
    rol_form = normalize_role(request.form.get('rol', user.rol))

    # Validaciones básicas (NO exigimos password al editar)
    if not not_empty(username, email):
        return render_template('users/edit_user.html', user=user, error="Nombre de usuario y email son obligatorios")
    if not is_valid_email(email):
        return render_template('users/edit_user.html', user=user, error="Email inválido")

    # Evitar duplicados en OTRO usuario
    other = Users.query.filter(
        or_(Users.email == email, Users.username == username),
        Users.id != id
    ).first()
    if other:
        return render_template('users/edit_user.html', user=user, error="Usuario o email ya está en uso")

    # Si NO es admin, no puede cambiar el rol
    es_admin = (session.get('rol') or '').lower() in {'admin', 'administrador'}
    if es_admin:
        if rol_form not in ALLOWED_ROLES:
            return render_template('users/edit_user.html', user=user, error=f"Rol inválido: {rol_form}")
        user.rol = rol_form
    # si no es admin, el rol queda como estaba

    # Guardar cambios
    user.username = username
    user.email    = email

    # Hashear solo si ingresaron una nueva contraseña
    if (password or '').strip():
        user.set_password(password)

    db.session.commit()

    # Si edité al usuario actualmente logueado, refresco la sesión
    if session.get('user_id') == user.id:
        session['username'] = user.username
        session['rol'] = user.rol

    flash("Usuario actualizado", "success")
    return redirect(url_for('routes_users.get_users'))

# ELIMINAR (POST) — solo admin
@routes_users.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('routes_users.get_users'))

    db.session.delete(user)
    db.session.commit()

    # Si borré al usuario logueado, lo deslogueo “de hecho”
    if session.get('user_id') == id:
        session.clear()

    flash("Usuario eliminado", "success")
    return redirect(url_for('routes_users.get_users'))
