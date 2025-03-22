# Flask Tutorial Blog

Este es un blog creado con Flask que incluye autenticación de usuarios y funcionalidades CRUD para posts.

## Características

- Sistema de autenticación (registro, inicio de sesión, cierre de sesión)
- Gestión de posts (crear, leer, actualizar, eliminar)
- Interfaz de usuario moderna y responsive
- Base de datos SQLite integrada

## Estructura del Proyecto

```
flask-tutorial/
├── flaskr/
│   ├── __init__.py
│   ├── auth.py
│   ├── blog.py
│   ├── db.py
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── blog/
│           ├── create.html
│           ├── update.html
│           └── index.html
└── instance/
    └── flaskr.sqlite
```

## Requisitos

- Python 3.6+
- Flask
- SQLite3

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Instala las dependencias:
   ```bash
   pip install flask
   ```
5. Inicializa la base de datos:
   ```bash
   flask --app flaskr init-db
   ```

## Uso

1. Ejecuta la aplicación:
   ```bash
   flask --app flaskr run
   ```
2. Abre tu navegador y ve a `http://localhost:5000`
3. Regístrate o inicia sesión
4. Crea, edita y elimina posts

## Funcionalidades Principales

### Autenticación
- Registro de usuarios
- Inicio de sesión
- Cierre de sesión
- Sesiones seguras

### Blog
- Crear nuevos posts
- Ver lista de posts
- Editar posts propios
- Eliminar posts propios
- Interfaz de usuario moderna

## Tecnologías Utilizadas

- Backend: Flask
- Frontend: HTML5, CSS3
- Base de datos: SQLite
- Gestión de sesiones: Flask-Login

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribución

¡Las contribuciones son bienvenidas! Por favor, crea un issue o pull request para sugerir mejoras.
