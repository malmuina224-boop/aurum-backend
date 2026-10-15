# AURUM Sweet Alchemy Backend

API REST con FastAPI, SQLAlchemy y Microsoft SQL Server para el frontend AURUM.

## Requisitos

- Python 3.11 o superior
- SQL Server con `AurumSweetAlchemyDB`
- Microsoft ODBC Driver 18 for SQL Server

## Configuración en Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` si tu servidor no se llama `localhost`.

## Ejecutar

```powershell
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`
Documentación Swagger: `http://127.0.0.1:8000/docs`

## Verificaciones

```powershell
python -m compileall app
pytest
```

## Endpoints iniciales

- `GET /api/v1/health`
- `GET /api/v1/productos`
- `GET /api/v1/productos/{id}`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/token`
- `GET /api/v1/auth/me`
- `GET /api/v1/pedidos/mis-pedidos`
- `POST /api/v1/pedidos`
- `GET /api/v1/facturas/mis-facturas`

Las contraseñas se almacenan como hash Argon2. Nunca guardes contraseñas sin hash.
