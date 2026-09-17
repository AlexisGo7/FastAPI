# device_systems

API REST para gestionar usuarios, dispositivos tecnologicos y prestamos con FastAPI, SQLAlchemy, SQLite y Alembic.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E)

## Resumen

`device_systems` es una API backend para controlar un inventario de equipos
tecnologicos y su historial de prestamos. El proyecto demuestra como pasar de
un CRUD de usuarios a un sistema relacional con migraciones, claves foraneas,
relaciones ORM, consultas con joins y reglas de negocio.

## Indice

- [Objetivo](#objetivo-de-la-actividad)
- [Funcionalidades](#funcionalidades-implementadas)
- [Arquitectura](#arquitectura)
- [Instalacion](#instalacion)
- [Migraciones](#migraciones-con-alembic)
- [Ejecucion](#ejecucion)
- [Endpoints](#endpoints-principales)
- [Pruebas](#pruebas-funcionales)
- [Evidencias](#evidencias-de-entrega)

## Objetivo de la actividad

Esta actividad evoluciona el CRUD de usuarios de la guia anterior hacia un sistema backend relacional. El objetivo principal es incorporar migraciones controladas con Alembic, asociaciones entre los modelos `User`, `Device` y `Loan`, y consultas avanzadas con `join`, filtros y relaciones.

La API conserva el recurso `/users` y agrega `/devices` y `/loans`. El sistema permite registrar usuarios y dispositivos, crear prestamos, impedir prestamos de dispositivos no disponibles, consultar historiales y devolver equipos actualizando su disponibilidad.

## Funcionalidades implementadas

- CRUD de usuarios persistido en SQLite.
- CRUD de dispositivos con numero de serie unico.
- Relaciones `User -> Loan`, `Device -> Loan` y `Loan -> User/Device`.
- Creacion de prestamos con validacion de usuario, dispositivo y disponibilidad.
- Devolucion de prestamos con fecha de retorno y disponibilidad restaurada.
- Historial de prestamos por usuario y por dispositivo.
- Filtros por estado, correo de usuario, tipo de dispositivo, marca y texto.
- Migraciones versionadas con Alembic.
- Validaciones Pydantic y respuestas documentadas en OpenAPI.

## Arquitectura

| Capa | Responsabilidad |
| --- | --- |
| `models` | Tablas, columnas, claves foraneas y relaciones SQLAlchemy. |
| `schemas` | Validacion de datos de entrada y salida con Pydantic. |
| `routes` | Endpoints HTTP y codigos de respuesta. |
| `services` | Consultas, reglas CRUD y transacciones. |
| `dependencies` | Sesion de base de datos por solicitud. |
| `alembic` | Migraciones versionadas de la base de datos. |

### Flujo de un prestamo

```mermaid
flowchart LR
  U[Usuario existente] --> L[POST /loans]
  D[Dispositivo disponible] --> L
  L --> A[Prestamo activo]
  A --> B[Dispositivo no disponible]
  B --> R[PATCH /loans/id/return]
  R --> H[Prestamo devuelto]
  H --> D2[Dispositivo disponible]
```

## Tecnologias

- Python 3.14
- FastAPI
- Uvicorn
- SQLAlchemy 2
- Alembic
- Pydantic 2
- email-validator
- SQLite

## Estructura del proyecto

```text
device_systems/
├── app/
│   ├── main.py
│   ├── database/connection.py
│   ├── dependencies/database_dependency.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   └── services/
│       ├── user_service.py
│       ├── device_service.py
│       └── loan_service.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── device_systems.db
├── requirements.txt
└── README.md
```

## Modelo de datos y relaciones

### User

Representa a las personas que utilizan el sistema. Conserva los campos `id`, `name`, `email`, `role`, `is_active` y `created_at`.

### Device

Representa los equipos disponibles para prestamo:

| Campo | Tipo | Restriccion |
| --- | --- | --- |
| `id` | Integer | Clave primaria |
| `name` | String | Obligatorio |
| `serial_number` | String | Obligatorio, unico e indexado |
| `device_type` | String | laptop, tablet, proyector, camara, router o monitor |
| `brand` | String | Opcional |
| `is_available` | Boolean | Por defecto `True` |
| `created_at` | DateTime | Fecha automatica |

### Loan

Representa el prestamo de un dispositivo a un usuario. Contiene `user_id` y `device_id` como claves foraneas, ademas de `loan_date`, `return_date` y `status`. Los estados permitidos son `active`, `returned` y `overdue`.

Un usuario puede tener muchos prestamos y un dispositivo puede aparecer en varios prestamos historicos. Cada prestamo pertenece exactamente a un usuario y a un dispositivo mediante `ForeignKey()` y `relationship()` con `back_populates`.

## Requisitos previos

- Python 3.11 o superior.
- Git.
- PowerShell o una terminal compatible con entornos virtuales.

La aplicacion utiliza SQLite, por lo que no requiere instalar un servidor de
base de datos adicional.

## Instalacion

Desde la raiz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Migraciones con Alembic

La base de datos se configura en `alembic.ini` con SQLite:

```text
sqlite:///./device_systems.db
```

La metadata de SQLAlchemy se carga en `alembic/env.py` desde los modelos de la aplicacion. Los comandos principales son:

```powershell
alembic history
alembic revision --autogenerate -m "create devices and loans tables"
alembic upgrade head
```

En este proyecto existe una migracion versionada en `alembic/versions/8d44b2c4a063_create_devices_and_loans_tables.py`, que crea las tablas `devices` y `loans` sobre la tabla `users` existente.

Para comprobar que no existen cambios de esquema pendientes:

```powershell
.\venv\Scripts\alembic.exe check
```

## Ejecucion

Primero aplica las migraciones y despues inicia la API:

```powershell
.\venv\Scripts\Activate.ps1
alembic upgrade head
python -m uvicorn app.main:app --reload
```

La API queda disponible en:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Para detener el servidor, presiona `Ctrl+C`.

## Endpoints principales

### Users

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/users` | Lista, filtra y ordena usuarios |
| `GET` | `/users/{user_id}` | Consulta un usuario |
| `POST` | `/users` | Crea un usuario |
| `PUT` | `/users/{user_id}` | Reemplaza un usuario |
| `PATCH` | `/users/{user_id}` | Actualiza parcialmente |
| `DELETE` | `/users/{user_id}` | Elimina un usuario |

### Devices

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/devices` | Lista y filtra dispositivos |
| `GET` | `/devices/{device_id}` | Consulta un dispositivo |
| `POST` | `/devices` | Registra un dispositivo |
| `PUT` | `/devices/{device_id}` | Actualiza completamente |
| `PATCH` | `/devices/{device_id}` | Actualiza parcialmente |
| `DELETE` | `/devices/{device_id}` | Elimina si no tiene historial |
| `GET` | `/devices/{device_id}/loans` | Consulta el historial del equipo |

Filtros disponibles en `GET /devices`: `device_type`, `is_available`, `brand` y `search`.

### Loans

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/loans` | Lista prestamos con filtros y relaciones |
| `GET` | `/loans/details` | Consulta detalles con usuario y dispositivo |
| `GET` | `/loans/{loan_id}` | Consulta un prestamo |
| `POST` | `/loans` | Crea un prestamo activo |
| `PATCH` | `/loans/{loan_id}/return` | Devuelve el dispositivo |
| `GET` | `/users/{user_id}/loans` | Consulta prestamos de un usuario |

Filtros disponibles en `/loans`: `status`, `user_email` y `device_type`.

Ejemplos de consultas:

```text
GET /devices?device_type=laptop&is_available=true
GET /devices?brand=lenovo&search=thinkpad
GET /loans?status=active&device_type=laptop
GET /loans/details?user_email=ana@example.com
GET /users/1/loans
GET /devices/1/loans
```

## Ejemplos de solicitudes

Crear un dispositivo:

```json
{
  "name": "ThinkPad T14",
  "serial_number": "LEN-2024-001",
  "device_type": "laptop",
  "brand": "Lenovo",
  "is_available": true
}
```

Crear un prestamo:

```json
{
  "user_id": 1,
  "device_id": 1
}
```

La respuesta detallada de un prestamo incluye el estado, las fechas y los datos basicos del usuario y del dispositivo.

Ejemplo de respuesta detallada:

```json
{
  "loan_id": 1,
  "status": "active",
  "loan_date": "2026-09-17T10:30:00",
  "return_date": null,
  "user": {
    "id": 1,
    "name": "Ana Perez",
    "email": "ana@example.com"
  },
  "device": {
    "id": 1,
    "name": "ThinkPad T14",
    "serial_number": "LEN-2024-001",
    "device_type": "laptop"
  }
}
```

## Manejo de errores

| Situacion | Codigo |
| --- | --- |
| Registro creado | `201 Created` |
| Consulta o actualizacion exitosa | `200 OK` |
| Eliminacion exitosa | `204 No Content` |
| Recurso inexistente | `404 Not Found` |
| Email o serial duplicado | `400 Bad Request` |
| Dispositivo no disponible o prestamo ya devuelto | `409 Conflict` |
| Datos invalidos o filtro no permitido | `422 Unprocessable Entity` |

## Pruebas funcionales

La implementacion fue verificada con un servidor Uvicorn en un puerto temporal:

- Migracion aplicada con `alembic upgrade head`.
- Usuario creado correctamente.
- Dispositivo creado correctamente.
- Prestamo creado y marcado como `active`.
- Segundo prestamo del mismo dispositivo rechazado con `409`.
- Consulta `/loans/details` con filtros y datos relacionados.
- Historial consultado desde `/users/{user_id}/loans` y `/devices/{device_id}/loans`.
- Dispositivo devuelto con `PATCH /loans/{loan_id}/return`.
- Disponibilidad restaurada a `true`.
- Segunda devolucion rechazada con `409`.

Validaciones tecnicas ejecutadas:

```powershell
python -m compileall -q app alembic
.\venv\Scripts\alembic.exe check
```

Resultado esperado:

```text
No new upgrade operations detected.
```

## Evidencias de entrega

Se deben anexar capturas o registros de:

1. `alembic init` y estructura de la carpeta Alembic.
2. `alembic revision --autogenerate`.
3. `alembic upgrade head` y `alembic history`.
4. Tablas `users`, `devices`, `loans` y sus relaciones.
5. Swagger UI con tags `Users`, `Devices` y `Loans`.
6. Creacion de usuario, dispositivo y prestamo.
7. Error al prestar un dispositivo no disponible.
8. Consultas con joins y filtros.
9. Devolucion y disponibilidad restaurada.

## Rama de trabajo

La actividad solicita una rama llamada:

```text
device_systems_alembic_relaciones
```

Despues de verificar los cambios, debe integrarse con `main` y publicarse en el repositorio GitHub del proyecto.

## Reflexion final

Alembic permite evolucionar la estructura de la base de datos de forma controlada y reproducible. Las relaciones garantizan la integridad entre usuarios, equipos y prestamos, mientras que los joins permiten responder consultas utiles sin duplicar datos en la API. Esta combinacion transforma un CRUD basico en un sistema backend preparado para crecer y mantener un historial confiable de operaciones.
