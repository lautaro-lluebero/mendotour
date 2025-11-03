from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.users import Users
from models.db import db

routes_auth = Blueprint('routes_auth', __name__)

@routes_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        raw   = request.form.get('password') or ''

        user = Users.query.filter_by(email=email).first()
        if user:
            if not user.is_hashed() and user.password == raw:
                user.set_password(raw)
                db.session.commit()

            if user.check_password(raw):
                session['logged_in'] = True
                session['user_id']   = user.id
                session['username']  = user.username
                session['rol']       = user.rol
                flash('¡Sesión iniciada!', 'success')
                return redirect(url_for('home'))  # <-- SIEMPRE Home

        flash('Email o contraseña incorrectos', 'error')

    return render_template('users/login.html')

@routes_auth.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('routes_auth.login'))
