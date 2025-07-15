import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from flaskr.db import get_db
from .forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db()
        error = None
        user_data = db.execute(
            'SELECT * FROM user WHERE username = ?', (form.username.data,)
        ).fetchone()

        if user_data is None or not check_password_hash(user_data['password'], form.password.data):
            error = 'Incorrect username or password.'

        if error is None:
            from . import load_user # Importar la función para cargar el usuario
            user = load_user(user_data['id'])
            login_user(user)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))