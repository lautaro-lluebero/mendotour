from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        is_logged = session.get('logged_in') or ('user_id' in session)
        if is_logged:
            return view(*args, **kwargs)
        flash('Necesitás iniciar sesión para continuar.', 'warning')
        next_url = request.full_path if request.query_string else request.path
        return redirect(url_for('routes_auth.login', next=next_url))
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        rol = (session.get('rol') or '').lower().strip()
        if rol in {'admin', 'administrador'}:
            return view(*args, **kwargs)
        flash('No tenés permisos de administrador para realizar esta acción.', 'danger')
        return redirect(url_for('routes_users.get_users'))
    return wrapped
