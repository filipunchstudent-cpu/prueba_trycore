# Gestión de proyectos con Valor Ganado

Aplicación web para administrar proyectos y actividades usando métricas de Valor Ganado.

## Tecnologías

- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** Vue 3, Vite
- **Base de datos local:** SQLite
- **Contenedores:** Docker y Docker Compose
- **Pruebas:** Pytest
- **Terminal, Git, pytest, pytest-cov, Ruff, Vitest, ESLint y Docker:** herramientas de implementación y verificación. Una respuesta de IA se aceptó solo después de comprobar código, resultados o documentación cuando correspondía.


## Métricas implementadas

Por cada actividad se calculan:

- PV: Planned Value
- EV: Earned Value
- CV: Cost Variance
- SV: Schedule Variance
- CPI: Cost Performance Index
- SPI: Schedule Performance Index
- EAC: Estimate at Completion
- VAC: Variance at Completion

El consolidado del proyecto se calcula sumando BAC, PV, EV y AC de sus actividades, y luego recalculando los indicadores del proyecto.

## Ejecutar datos demo

El proyecto incluye un script para cargar datos de ejemplo en la base de datos. Este script crea un proyecto llamado `Proyecto demo EVM` con tres actividades: `Descubrimiento`, `Desarrollo` y `Pruebas`.

Desde la raíz del proyecto ejecuta:

```bash
cd ~/PycharmProjects/evm-project
python3 -m backend.app.init_db
```


## Ejecución local

Backend:

```bash
cd ~/PycharmProjects/evm-project
python3 -m backend.app.init_db
python3 -m uvicorn backend.app.main:app --reload --port 8000
```

Frontend:
```bash
cd ~/PycharmProjects/evm-project/frontend
npm install
npm run dev
```

## Inicio recomendado: Docker

Requisitos: Docker Engine o Docker Desktop con Docker Compose. Ejecuta los comandos desde la carpeta que contiene este README.
```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```
En Windows PowerShell, el primer comando es `Copy-Item .env.example .env`. Si tu instalación proporciona el ejecutable independiente, usa `docker-compose` en lugar de `docker compose` en todos los comandos.
El primer arranque descarga las imágenes, instala las dependencias, y carga un proyecto de demostración con tres actividades. Espera a que los servicios estén saludables en `docker compose ps`.

| Recurso | Dirección |
| --- | --- |
| Dashboard | <http://localhost:5173> |
| Swagger / OpenAPI | <http://localhost:8000/api-docs> |
| Estado de API | <http://localhost:8000/api/health> |
| OpenAPI en JSON | <http://localhost:8000/openapi.json> |

## Estructura

```text
backend/                  API FastAPI, persistencia y tests
frontend/                 Dashboard Vue 3 con Vite y Vitest
compose.yaml              API y frontend
.github/workflows/ci.yml   Comprobaciones automáticas
docs/                     Explicación, pruebas
AI_PROCESS.md             Registro del proceso de trabajo con IA
```



