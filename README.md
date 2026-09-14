# device_systems

API REST para la gestión persistente de usuarios, desarrollada con FastAPI,
SQLAlchemy, Pydantic y SQLite.

## Objetivo de la actividad

El objetivo principal de esta actividad es evolucionar la aplicación
`device_systems` para reemplazar el almacenamiento temporal en memoria por una
base de datos relacional real.

La aplicación permite crear, consultar, filtrar, actualizar y eliminar
usuarios mediante operaciones CRUD. Durante el desarrollo se aplican los
principios de separación entre modelos SQLAlchemy y schemas Pydantic,
validaciones de datos, restricciones de base de datos, manejo de errores y
documentación automática con Swagger/OpenAPI.

## Alcance funcional

La API permite:

- Crear usuarios y almacenarlos en SQLite.
- Consultar usuarios individuales o listarlos.
- Filtrar por rol y estado activo.
- Ordenar por nombre o fecha de creación.
- Actualizar usuarios completamente mediante `PUT`.
- Actualizar usuarios parcialmente mediante `PATCH`.
- Eliminar usuarios mediante `DELETE`.
- Validar nombres, correos electrónicos, roles y estados.
- Controlar correos duplicados y usuarios inexistentes.

## Tecnologías utilizadas

- Python 3.14
- FastAPI
- Uvicorn
- SQLAlchemy 2
- Pydantic 2
- email-validator
- SQLite

## Estructura del proyecto

```text
device_systems/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── dependencies/
│   │   └── database_dependency.py
│   ├── models/
│   │   └── user_model.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── schemas/
│   │   └── user_schema.py
│   └── services/
│       └── user_service.py
├── device_systems.db
├── requirements.txt
└── README.md
```

## Persistencia con SQLAlchemy

La aplicación utiliza SQLite mediante la URL:

```python
sqlite:///./device_systems.db
```

El archivo `app/database/connection.py` configura el engine, la sesión
`SessionLocal` y la clase declarativa `Base`. La dependencia `get_db` crea una
sesión para cada solicitud y la cierra al finalizar.

El modelo `User` representa la tabla `users` con los siguientes campos:

| Campo | Tipo | Restricción |
| --- | --- | --- |
| `id` | Integer | Clave primaria e índice |
| `name` | String | Obligatorio |
| `email` | String | Obligatorio, único e indexado |
| `role` | String | Obligatorio |
| `is_active` | Boolean | Obligatorio, valor predeterminado `True` |
| `created_at` | DateTime | Fecha de creación automática |

## Modelo SQLAlchemy y schema Pydantic

El modelo SQLAlchemy define cómo se almacenan los datos en la base de datos,
incluyendo tipos, índices y restricciones.

Los schemas Pydantic definen los datos que la API recibe y devuelve. También
validan que el nombre tenga al menos tres caracteres, que el email tenga un
formato válido y que el rol sea `admin`, `support` o `user`.

La aplicación utiliza estos schemas:

- `UserCreate`: datos necesarios para crear un usuario.
- `UserUpdate`: datos completos requeridos por `PUT`.
- `UserPatch`: campos opcionales permitidos por `PATCH`.
- `UserResponse`: representación pública del usuario.

## Instalación

Desde la carpeta raíz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si el entorno virtual ya existe, solo es necesario activarlo e instalar las
dependencias.

## Ejecución

```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

> El módulo correcto es `app.main:app`, porque el archivo `main.py` está
> dentro del paquete `app`.

## Endpoints

| Método | Ruta | Descripción | Respuesta principal |
| --- | --- | --- | --- |
| `GET` | `/` | Verificar que la API está activa | `200 OK` |
| `POST` | `/users` | Crear un usuario | `201 Created` |
| `GET` | `/users` | Listar, filtrar y ordenar usuarios | `200 OK` |
| `GET` | `/users/{user_id}` | Buscar un usuario por ID | `200 OK` |
| `PUT` | `/users/{user_id}` | Reemplazar todos los datos | `200 OK` |
| `PATCH` | `/users/{user_id}` | Actualizar campos específicos | `200 OK` |
| `DELETE` | `/users/{user_id}` | Eliminar un usuario | `204 No Content` |

### Parámetros de consulta de `GET /users`

- `role`: `admin`, `support` o `user`.
- `is_active`: `true` o `false`.
- `order_by`: `name` o `created_at`.

### Ejemplo de creación

```json
{
	"name": "Ana García",
	"email": "ana@example.com",
	"role": "user",
	"is_active": true
}
```

## Manejo de errores

| Situación | Código |
| --- | --- |
| Datos inválidos, email incorrecto o rol no permitido | `422 Unprocessable Entity` |
| Email duplicado | `400 Bad Request` |
| Usuario no encontrado | `404 Not Found` |
| Usuario creado correctamente | `201 Created` |
| Consulta o actualización correcta | `200 OK` |
| Eliminación correcta | `204 No Content` |

## Pruebas funcionales realizadas

La API fue verificada con un servidor Uvicorn y se comprobaron los casos
principales de la guía:

- Creación de un usuario válido: `201 Created`.
- Creación con email repetido: `400 Bad Request`.
- Listado con filtros por rol y estado: `200 OK`.
- Actualización parcial con `PATCH`: `200 OK`.
- Eliminación de un usuario: `204 No Content`.
- Consulta del usuario eliminado: `404 Not Found`.

También se verificó la importación de la aplicación, la compilación de los
módulos Python y la generación del esquema OpenAPI.

## Evidencias para la entrega

Para completar la evidencia de aprendizaje se recomienda anexar al repositorio
o al documento de entrega:

1. Captura de la estructura del proyecto.
2. Captura de la base de datos `device_systems.db` y la tabla `users`.
3. Captura de Swagger UI con los endpoints publicados.
4. Capturas de creación, consulta, actualización y eliminación.
5. Capturas de los errores `400`, `404` y `422`.
6. Este README como explicación técnica del proyecto.

## Reflexión final

La persistencia permite que los usuarios no se pierdan cuando la aplicación se
reinicia. SQLAlchemy facilita la comunicación entre FastAPI y la base de datos
mediante objetos Python, mientras que Pydantic protege la entrada y salida de
la API mediante schemas y validaciones. Separar ambas responsabilidades hace
que el sistema sea más claro, mantenible y preparado para crecer hacia otros
motores de base de datos y nuevos recursos.

## Guion breve para la socialización

En la presentación se pueden explicar estos puntos:

1. Se reemplazó la lista en memoria por SQLite y SQLAlchemy.
2. Se creó el modelo `User` con constraints y fecha de creación.
3. Se separaron los modelos de persistencia de los schemas de la API.
4. Se implementaron las operaciones CRUD, filtros y ordenamiento.
5. Se agregaron validaciones Pydantic y errores HTTP.
6. Se verificó la API mediante Swagger y pruebas funcionales.
