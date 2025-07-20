
# flaskR

Proyecto Flask + Supabase desplegado en Vercel

<p align="center">
[LinkedIn: Hillkirk Lautaro](https://www.linkedin.com/in/hillkirklautaro/) |
[Vercel](https://vercel.com/) |
[Supabase](https://supabase.com/) |
[Flask](https://flask.palletsprojects.com/)
</p>

## Descripción
Este proyecto es una aplicación web construida con Flask y Jinja2, que permite a los usuarios completar una encuesta y almacena las respuestas en una base de datos Supabase. El frontend utiliza plantillas HTML modernas y CSS personalizado. El backend valida los datos y protege los formularios con CSRF.

## Características
- Página principal con saludo personalizado y navegación.
- Página "About" con información del proyecto.
- Página "Encuesta" con formulario seguro y validación.
- Almacenamiento de respuestas en Supabase.
- Despliegue en Vercel.

## Estructura del proyecto
```
flaskR/
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── static/
│   │   └── css/
│   │       └── styles.css
│   └── templates/
│       ├── index.html
│       ├── about.html
│       └── encuesta.html
├── requirements.txt
├── vercel.json
├── .env (no subir a GitHub)
```

## Instalación y ejecución local
1. Clona el repositorio.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` con tus claves de Supabase y una `SECRET_KEY`.
4. Ejecuta la app:
   ```
   flask run
   ```

## Variables de entorno
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Secret Key de Supabase
- `SECRET_KEY`: Clave secreta para CSRF y sesiones

## Despliegue en Vercel
Configura las variables de entorno en el dashboard de Vercel y sube el proyecto.

---
¿Quieres aprender Flask, Supabase y despliegue en Vercel? ¡Este proyecto es un gran punto de partida!

Si te gustó, podes forkear el repo y contribuir. Todas las Pull Request seran analizadas, gracias.

