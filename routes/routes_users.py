from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.users import Users
import re

routes_users = Blueprint('routes_users', __name__, url_prefix='/users')

# ---------- Helpers de validación ----------
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email))

def not_empty(*vals) -> bool:
    return all(v and str(v).strip() for v in vals)

# Opcional: lista blanca de roles aceptados
ALLOWED_ROLES = {"admin", "administrador", "user", "cliente", "editor"}

def normalize_role(rol: str) -> str:
    """Normaliza variantes comunes para que sean consistentes."""
    if not rol:
        return "cliente"
    r = rol.strip().lower()
    # if r == "administrador": r = "admin"
    # if r == "cliente": r = "user"
    return r

# ---------- CRUD ----------

# LISTAR
@routes_users.route('/', methods=['GET'])
def get_users():
    users = Users.query.order_by(Users.id.asc()).all()
    return render_template('users/users.html', users=users)

# CREAR
@routes_users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        rol      = normalize_role(request.form.get('rol', 'cliente'))

        # Validaciones básicas
        if not not_empty(username, email, password):
            return render_template('users/register.html', error="Todos los campos son obligatorios")
        if not is_valid_email(email):
            return render_template('users/register.html', error="Email inválido")
        if rol not in ALLOWED_ROLES:
            return render_template('users/register.html', error=f"Rol inválido: {rol}")

        # Duplicados por email O username
        existing = Users.query.filter(or_(Users.email == email, Users.username == username)).first()
        if existing:
            msg = "Ese email ya está registrado" if existing.email == email else "Ese usuario ya existe"
            return render_template('users/register.html', error=msg)

        # Crear usuario (tu modelo ya hashea en __init__ con set_password)
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

# EDITAR (form)
@routes_users.route('/update/<int:id>', methods=['GET'])
def edit_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('routes_users.get_users'))
    return render_template('users/edit_user.html', user=user)

# EDITAR (guardar)
@routes_users.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    user = Users.query.get(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('routes_users.get_users'))

    username = request.form.get('username', '').strip()
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')  # puede venir vacío
    rol      = normalize_role(request.form.get('rol', user.rol))

    # Validaciones: NO exigimos password al editar
    if not not_empty(username, email):
        return render_template('users/edit_user.html', user=user, error="Nombre de usuario y email son obligatorios")
    if not is_valid_email(email):
        return render_template('users/edit_user.html', user=user, error="Email inválido")
    if rol not in ALLOWED_ROLES:
        return render_template('users/edit_user.html', user=user, error=f"Rol inválido: {rol}")

    # Evitar duplicados en OTRO usuario
    other = Users.query.filter(
        or_(Users.email == email, Users.username == username),
        Users.id != id
    ).first()
    if other:
        return render_template('users/edit_user.html', user=user, error="Usuario o email ya está en uso")

    # Guardar cambios
    user.username = username
    user.email    = email
    user.rol      = rol

    # Hashear solo si ingresaron una nueva contraseña
    if (password or '').strip():
        user.set_password(password)   # <<< CLAVE: NO guardar en texto plano

    db.session.commit()

    # Si edité al usuario actualmente logueado, refresco la sesión
    if session.get('user_id') == user.id:
        session['username'] = user.username
        session['rol'] = user.rol

    flash("Usuario actualizado", "success")
    return redirect(url_for('routes_users.get_users'))

# ELIMINAR (POST)
@routes_users.route('/delete/<int:id>', methods=['POST'])
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
