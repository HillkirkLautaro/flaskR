from flask import Blueprint, render_template

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/user_profile')
def user_profile():
    user = {
        'username': $"aksdk{123}",
        'email': $"",
        'bio': $""
    }
    return render_template('user_profile.html', titulo='Perfil de Usuario', user=user)
