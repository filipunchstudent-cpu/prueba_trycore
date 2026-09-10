# Guía de explicación del proyecto

## Objetivo
El proyecto permite administrar proyectos y actividades usando Valor Ganado. Cada actividad tiene presupuesto, porcentaje planeado, porcentaje real y costo real. Con esos datos se calculan métricas de desempeño de costo y cronograma.

## Arquitectura

La aplicación está separada en backend y frontend (arquitectura monorepo).
El backend está hecho con FastAPI. Expone endpoints REST para proyectos y actividades. La lógica de negocio está en `backend/app/services/evm.py`, separada de los endpoints.
El frontend está hecho con Vue 3. Consume la API y muestra un dashboard con métricas, tabla de actividades, formularios y una gráfica simple de PV, EV y AC.
La base de datos usa SQLAlchemy. En desarrollo se usa SQLite porque es fácil de ejecutar localmente, pero la conexión se configura con `DATABASE_URL`, así que se puede cambiar a PostgreSQL.

## Fórmulas

PV = BAC * porcentaje planeado / 100
EV = BAC * porcentaje real / 100
CV = EV - AC
SV = EV - PV
CPI = EV / AC
SPI = EV / PV
EAC = BAC / CPI
VAC = BAC - EAC

## Decisión importante

La decisión principal fue mantener los cálculos en el backend. Vue no calcula Valor Ganado; solo muestra lo que devuelve la API. Esto evita duplicar lógica y mantiene una única fuente de verdad.

## Pruebas
Las pruebas unitarias validan las fórmulas y casos borde como AC en cero, PV en cero y proyecto sin actividades.
Las pruebas de integración validan los endpoints reales de FastAPI: creación, consulta, actualización, eliminación, validaciones y errores 404.