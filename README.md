
# Talk-Easy Backend

Este repositorio contiene los microservicios backend de la aplicación **Talk-Easy**, implementados con FastAPI y organizados en una arquitectura de microservicios con Docker Compose.

---

## Estructura del proyecto

- **auth-api/**: Microservicio de autenticación y gestión de usuarios.
- **tagging-api/**: Microservicio para gestión y etiquetado inteligente de mensajes.
- **talkeasy/**: Microservicio principal para mensajería y lógica de negocio.
- **api-gateway/**: Gateway para orquestar las peticiones a los distintos microservicios.
- **wait-for-it.sh**: Script para esperar a que las bases de datos estén disponibles antes de iniciar las APIs.

---

## Requisitos previos

- Docker y Docker Compose instalados.
- Clonar el repositorio completo con todos los servicios.
- Archivos `.env` configurados en las carpetas `auth-api`, `tagging-api` y `talkeasy` (ver más abajo).

---

## Configuración de variables de entorno

Cada microservicio tiene su propio archivo `.env` donde se definen variables clave como credenciales de base de datos y configuración específica.

Ejemplos de variables comunes en `.env`:

```env
POSTGRES_USER=usuario
POSTGRES_PASSWORD=contraseña
POSTGRES_DB=nombre_basedatos
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_basedatos
SECRET_KEY=clave_secreta_para_jwt
```

> **Nota:** No subir los archivos `.env` con información sensible al repositorio público.

---

## Cómo ejecutar el proyecto con Docker Compose

1. Clonar el repositorio.

2. Colocar los archivos `.env` correspondientes en las carpetas:
   - `auth-api/.env`
   - `tagging-api/.env`
   - `talkeasy/.env`
  (Cada servicio tiene su .env.example para ver el ejemplo)

3. Generar claves pública y privada para JWT

Para la autenticación JWT se utilizan claves RSA pública y privada para firmar y verificar los tokens.
- Para generar las claves, abre una terminal y ejecuta:

```bash
    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in private_key.pem -out public_key.pem
```
Coloca private_key.pem en la ruta base de auth-api y public_key.pem en el directorio de gateway-api.

4. Ejecutar:

```bash
docker-compose up --build
```

Esto levantará todos los contenedores:

- Bases de datos PostgreSQL para cada servicio.
- Microservicios `auth-api`, `tagging-api`, `talkeasy-api`.
- API Gateway en el puerto 8000, que orquesta las peticiones.

4. Acceder a la API Gateway en: `http://localhost:8000`
   

---

## Detalles técnicos

- Las bases de datos están persistidas en volúmenes Docker para mantener datos entre reinicios.
- El script `wait-for-it.sh` se usa para garantizar que las bases de datos estén listas antes de iniciar los servicios.
- Cada microservicio inicializa su base de datos ejecutando `init_db.py` antes de arrancar el servidor.
- El API Gateway unifica los endpoints y redirige las peticiones a los servicios correspondientes.
- ¡IMPORTANTE!: El docker-compose esta configurado para solo exponer los endpoints de GatewayAPI, el resto de apis estan en una red interna y no se puede acceder a ellas desde fuera del contenedor (Esta configuración simplifica la autenticación y seguridad en todo el proyecto).
---

## Desarrollo y testing

- Los servicios están configurados con hot-reload para facilitar el desarrollo (`uvicorn --reload`).
- Puedes acceder a la documentación automática de la API (Swagger UI) visitando, por ejemplo:
  - `http://localhost:8000/docs` (Gateway)

---

## Buenas prácticas

- Mantener los archivos `.env` fuera del control de versiones para proteger credenciales.
- Usar ramas específicas para desarrollo y producción.
- Ejecutar `docker-compose down` para parar y eliminar contenedores.

---

Si tienes dudas o necesitas ayuda, revisa la documentación oficial de FastAPI, PostgreSQL, Docker y el script `wait-for-it.sh`.
