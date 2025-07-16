import sys
import os

sys.path.insert(0, os.path.dirname(__file__))  # agrega carpeta actual a sys.path

from app import app
handler = app
