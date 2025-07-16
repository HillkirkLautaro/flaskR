import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

# Esto es lo que Vercel busca
handler = app
