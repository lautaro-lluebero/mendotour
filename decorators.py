from functools import wraps
from flask import session, redirect, url_for, flash, request

# Helpers
def _is_admin() -> bool:
    return (session.get('rol') or '').lower().strip() in {'admin', 'administrador'}

# Decorators
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        is_logged = session.get('logged_in') or ('user_id' in session)
        if is_logged:
            return view(*args, **kwargs)
        flash('Necesitás iniciar sesión para continuar.', 'warning')
        # preservar destino para volver post-login
        next_url = request.full_path if request.query_string else request.path
        return redirect(url_for('routes_auth.login', next=next_url))
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if _is_admin():
            return view(*args, **kwargs)
        flash('No tenés permisos de administrador para realizar esta acción.', 'danger')
        # Importante: redirigir a una ruta pública para evitar bucles
        return redirect(url_for('home'))
    return wrapped

def owner_or_admin(view):
    """
    Permite acceder si:
      - el usuario logueado es el dueño del recurso (id en la URL), o
      - es administrador.
    Úsalo en rutas como /users/update/<int:id>
    """
    @wraps(view)
    def wrapped(id, *args, **kwargs):
        me_id = session.get('user_id')
        if me_id == id or _is_admin():
            return view(id, *args, **kwargs)
        flash('No tenés permisos para editar ese usuario.', 'danger')
        return redirect(url_for('home'))
    return wrapped
