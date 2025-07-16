from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from . import supabase

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    try:
        # Obtener todos los posts y hacer un JOIN para traer el email del autor
        res = supabase.table('posts').select('*, profiles(email)').order('created_at', desc=True).execute()
        posts = res.data
    except Exception as e:
        posts = []
        flash(f'Error al cargar los posts: {e}', 'danger')
    return render_template('main/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if not g.user:
        flash('Debes iniciar sesión para crear un post.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        content = request.form['content']
        if not content or len(content) > 280:
            flash('El contenido no puede estar vacío y debe tener menos de 280 caracteres.', 'danger')
        else:
            try:
                supabase.table('posts').insert({
                    'content': content,
                    'author_id': g.user
                }).execute()
                flash('Post creado exitosamente.', 'success')
                return redirect(url_for('main.index'))
            except Exception as e:
                flash(f'Error al crear el post: {e}', 'danger')

    return render_template('main/create.html')

@bp.route('/profile/<user_id>')
def profile(user_id):
    try:
        # Obtener los posts del usuario
        posts_res = supabase.table('posts').select('*').eq('author_id', user_id).order('created_at', desc=True).execute()
        user_posts = posts_res.data

        # Obtener el email del perfil
        profile_res = supabase.table('profiles').select('email').eq('id', user_id).single().execute()
        profile_email = profile_res.data['email'] if profile_res.data else None

    except Exception as e:
        user_posts = []
        profile_email = None
        flash(f'Error al cargar el perfil: {e}', 'danger')

    return render_template('main/profile.html', posts=user_posts, profile_email=profile_email)
