from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import supabase

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            # Crear el perfil del usuario en la tabla 'profiles'
            supabase.table('profiles').insert({
                'id': res.user.id,
                'email': res.user.email
            }).execute()
            flash('Registro exitoso. Por favor, revisa tu email para confirmar tu cuenta.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error en el registro: {e}', 'danger')
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user'] = res.user.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Error al iniciar sesión: {e}', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
        session.pop('user', None)
        flash('Has cerrado sesión.', 'success')
    except Exception as e:
        flash(f'Error al cerrar sesión: {e}', 'danger')
    return redirect(url_for('main.index'))
