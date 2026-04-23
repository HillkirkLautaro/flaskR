# ☁️ Flaskr (PROYECTO DESCONTINUADO)

Microblog ligero y open-source hecho en **Flask**, con Tablas en **Supabase**, desplegado en **Vercel**.

[Vercel](https://flaskr-topaz.vercel.app/)
- **Demo**: https://flaskr-topaz.vercel.app/ 
- **Código fuente**: [GitHub](https://github.com/HillkirkLautaro/flaskR)

---

## 🚀 Funcionalidades

- 📝 Publicaciones tipo microblog (sin algoritmos ni filtros)
- 👤 Registro de usuario con seguridad (reCAPTCHA + hashing de contraseña)
- 📊 Encuestas anónimas con límite de 2 envíos por IP/hora
- 🕵️‍♂️ Seguridad básica: protección CSRF, saneamiento de input
- 🧩 Open source: podés clonar, modificar y desplegar por tu cuenta

---

## 🛠 Tech Stack

- **Backend**: Python + Flask + Flask-WTF  
- **Base de datos**: Supabase (PostgreSQL)  
- **Despliegue**: Vercel (serverless functions)  
- **Frontend**: Plantillas Jinja2 + CSS minimalista

---

Para instalar usar "git clone", crear un entorno virtual. ejecutar "pip install -r requirements.txt". Crear cuenta en supabase y crear un archivo ".env" con SUPABASE_URL="http""s""://tu-proyecto.supabase.co
SUPABASE_KEY=tu_api_key. Las claves que te da supabase al crear cuenta. 

Despues ejecutar esta query de sql "-- Tabla de usuarios
CREATE TABLE public.users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  username varchar(32) NOT NULL UNIQUE,
  email varchar(100) NOT NULL UNIQUE,
  password_hash text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  is_active boolean NOT NULL DEFAULT true
);

-- Tabla de encuestas
CREATE TABLE public.encuestas (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  opinion text NOT NULL,
  date_time timestamptz NOT NULL DEFAULT now(),
  ip_address varchar(45) NOT NULL
);

-- Índices útiles
CREATE INDEX idx_encuestas_ip_address ON public.encuestas (ip_address);
CREATE INDEX idx_encuestas_date_time ON public.encuestas (date_time);"

Ejecutar main.py para correr la pagina.

---

# Mejoras..

Estoy atento a PR que mejoren la webapp.