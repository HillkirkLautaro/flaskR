from .main import main_bp
from .encuesta import encuesta_bp
from .auth import auth_bp
from .user_profile import user_profile_bp

all_blueprints = [main_bp, encuesta_bp, auth_bp, user_profile_bp]
