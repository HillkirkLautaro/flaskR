## Esquema de la Base de Datos en Supabase

Este archivo describe las tablas necesarias para el MVP del microblog.

### Tabla `profiles`

Esta tabla almacenará información pública de los usuarios. Se vincula a la tabla `users` de Supabase Auth a través del `id`.

- **Nombre de la tabla:** `profiles`
- **Columnas:**
  - `id` (uuid, Clave Primaria): Corresponde al `id` del usuario en `auth.users`.
  - `email` (text, no nulo): El email del usuario.
  - `created_at` (timestamp with time zone, por defecto `now()`): Fecha de creación del perfil.

**Política de Seguridad (RLS):** Habilitar RLS. Permitir lectura pública para todos.

### Tabla `posts`


- **Nombre de la tabla:** `posts`
- **Columnas:**
  - `id` (bigint, Clave Primaria, autoincremental): Identificador único del post.
  - `author_id` (uuid, Clave Foránea a `profiles.id`): El ID del autor del post.
  - `content` (text, no nulo): El contenido del post (máx 280 caracteres).
  - `created_at` (timestamp with time zone, por defecto `now()`): Fecha de creación del post.

**Política de Seguridad (RLS):** Habilitar RLS. Permitir lectura pública para todos. Permitir inserción solo a usuarios autenticados. Permitir borrado/actualización solo al autor del post.
