# Proceso de trabajo con IA

## Por que elegi las herramientas de IA usadas

Elegí chatgpt, porque fuera de ser la herramienta en la que mejor tengo destreza, codex y sus modelos de pago pueden ser de gran ayuda y adicional es uno de los que menor coste tiene en el mercado en estos momentos,


### 1. Petición inicial,

```text
Actúa como un Project Manager / especialista en Earned Value Management (EVM) con experiencia práctica en la metodología del Project Management Institute (PMI).
Necesito que prepares una explicación muy clara, breve y práctica sobre:
Qué es PMI.
Qué es Earned Value Management (EVM) o Gestión del Valor Ganado.
Qué significa Earned Value (EV) o Valor Ganado.
Cómo interpretar las principales métricas de EVM que utilizaremos en nuestra aplicación.
Fuente y rigor
Antes de responder, verifica la información contra documentación oficial publicada por PMI. Prioriza fuentes de PMI sobre cualquier otra fuente.
Si alguna de las fórmulas proporcionadas representa solamente una de varias alternativas reconocidas por PMI, indícalo brevemente para evitar presentarla como la única fórmula válida.

Fórmulas que debes explicar
BAC — Budget at Completion: presupuesto total aprobado del proyecto.
PV — Planned Value: % planificado × BAC
EV — Earned Value: % completado × BAC
AC — Actual Cost: costo real incurrido por el trabajo realizado.
CV — Cost Variance: EV − AC
SV — Schedule Variance: EV − PV
CPI — Cost Performance Index: EV / AC
SPI — Schedule Performance Index: EV / PV
EAC — Estimate at Completion: BAC / CPI
VAC — Variance at Completion: BAC − EAC

Forma de explicarlo
Explícalo como si estuvieras enseñándole EVM por primera vez a un colega ingeniero que nunca ha trabajado con PMI.
No quiero una explicación académica ni demasiado extensa. Usa lenguaje profesional pero sencillo.
Para cada métrica proporciona:
Nombre en inglés y español.
Fórmula.
Qué pregunta responde.
Cómo interpretar un resultado bueno o malo.
Un ejemplo numérico pequeño, solamente cuando ayude a entenderla.
BAC = 1.000
Planned % = 50%
Actual % = 40%
AC = 450

A partir de estos datos explica brevemente cómo se obtienen PV, EV, CV, SV, CPI, SPI y EAC.
Punto clave que quiero que quede claro

Explica la diferencia entre:

PV: cuánto trabajo planeábamos haber realizado.
EV: cuánto trabajo realmente hemos realizado, expresado en términos del presupuesto.
AC: cuánto dinero realmente hemos gastado.

Después conecta estas tres variables para explicar que:

CV y CPI evalúan principalmente el desempeño de costos.
SV y SPI evalúan el desempeño respecto al cronograma.

Aclara también la interpretación general:
CV > 0 → favorable en costos.
CV < 0 → desfavorable en costos.
SV > 0 → favorable respecto al plan.
SV < 0 → desfavorable respecto al plan.
CPI > 1 → favorable en costos.
CPI < 1 → desfavorable en costos.
SPI > 1 → favorable respecto al plan.
SPI < 1 → desfavorable respecto al plan.
Formato de respuesta

Organiza la respuesta exactamente en estas secciones:

1. ¿Qué es PMI?
Máximo 2–3 párrafos.

2. ¿Qué es Earned Value Management?
Explicación sencilla en máximo 1–2 párrafos.

3. Las tres variables fundamentales
Presenta PV, EV y AC en una tabla.

4. Fórmulas principales
Presenta las fórmulas en una tabla con:
| Métrica | Fórmula | ¿Qué me dice? | Interpretación |

5. Ejemplo rápid
Utiliza los valores del ejemplo y calcula los indicadores principales.

6. Cómo leer el resultado
Termina con una explicación de máximo 5 líneas que permita a un usuario entender rápidamente si el proyecto está:

dentro/fuera de presupuesto;
adelantado/atrasado;
y cuál sería su costo estimado al finalizar.
Restricciones
Sé conciso y directo.
No incluyas historia extensa de PMI.
No agregues fórmulas avanzadas como TCPI, ETC o EAC alternativas salvo que sean necesarias para aclarar una posible ambigüedad.
No inventes definiciones.
Distingue claramente entre lo que es una definición de PMI y una simplificación didáctica.
Al final incluye una pequeña sección "Fuentes PMI" con los enlaces a las páginas de PMI utilizadas.
```

### 2. Petición arquitectura simple frontend y backend
```text
Actúa como arquitecto de software senior. Necesito diseñar una arquitectura simple para una aplicación de gestión de proyectos con Valor Ganado.

El sistema debe tener:
- Arquitectura monorepo.
- Backend en Python con FastAPI.
- Frontend en Vue 3.
- Base de datos relacional sencilla sqlite3.
- CRUD de proyectos.
- CRUD de actividades.
- Cálculo de métricas EVM: PV, EV, CV, SV, CPI, SPI, EAC y VAC.
- Separación clara entre lógica de negocio, API, base de datos y frontend.

Dame una arquitectura, con estructura de carpetas, responsabilidades de cada capa.
```

### 3. Petición codigo simple fastapi
```text
Actúa como desarrollador senior de Python. Necesito crear un backend simple con FastAPI para una aplicación de Valor Ganado.

Requisitos:
- Crear endpoints REST para proyectos y actividades.
- Usar SQLAlchemy con SQLite.
- Separar la lógica EVM en un servicio independiente.
- Implementar las fórmulas PV, EV, CV, SV, CPI, SPI, EAC y VAC.
- Evitar lógica de negocio dentro de los endpoints.
- Agregar validaciones básicas con Pydantic.
- Incluir Swagger en /api-docs.
- Mantener el código sencillo y fácil de explicar.
- Usar tests para validar las métricas.

Dame el código por archivos, indicando qué va en cada archivo y cómo ejecutarlo localmente.
```

### 3. Petición codigo simple vue.js
```text
Actúa como desarrollador frontend senior especializado en Vue 3. Necesito crear un frontend simple para consumir una API FastAPI de Valor Ganado.

Requisitos:
- Usar Vue 3 con Vite.
- Consumir endpoints de proyectos y actividades.
- Mostrar un dashboard con proyectos, actividades y métricas EVM.
- Crear formularios para agregar proyectos y actividades.
- Permitir editar y eliminar actividades.
- Mostrar métricas como BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC y VAC.
- Agregar una gráfica simple de PV, EV y AC sin usar librerías externas.
- Mantener el código sencillo, claro y fácil de explicar en un video.

Dame el código por archivos, incluyendo App.vue, api.js, main.js, style.css, package.json y vite.config.js.
```

### 3. Petición pipeline de docker
```text
Actúa como ingeniero DevOps. Necesito crear una configuración simple con Docker para una aplicación con backend FastAPI y frontend Vue.

El proyecto tiene:
- Backend en Python con FastAPI.
- Frontend en Vue 3 con Vite.
- Base de datos SQLite para desarrollo.
- Script de datos demo en backend.app.init_db.

Necesito:
- Dockerfile para backend.Dame una arquitectura, con estructura de carpetas, responsabilidades de cada capa.
- Dockerfile para frontend.
- Configuración Nginx para servir el frontend.
- compose.yaml para levantar backend y frontend.
- Comandos para ejecutar, detener y validar la aplicación.
- Explicación sencilla para documentarlo en README.

Dame los archivos completos y comandos de ejecución.
```

## Aprendizaje de EVM y validación de las fórmulas

Dentro del prompt se solicitó explicitamente que consulte la documentación oficial y trajera ejemplos y también se pidió que la explicación fuera a un colega que no sabe nada y ni entiende de PMI lo que me facilitó la interpretación de las métricas.
Para validar números se utilizó el ejemplo que arrojó la primera consulta realizada por prompt.
La conclusión a la que llegué es que la distinción fundamental es que PV representa el trabajo que debía estar terminado a presupuesto, EV representa el trabajo realmente terminado a presupuesto y AC es lo gastado. Porcentajes como 25 se convierten en 0,25 antes de multiplicar por BAC. EAC = BAC/CPI supone que la eficiencia actual continúa; SV es una diferencia monetaria, no una duración en días.

## Dos decisiones donde no seguí lo que la IA me sugirió

*  Los samples para los assertions no los estaba entregando bien debido a que en los tests no estaba comparando bien los números decimales, hice las respectivas correcciones
*  Preferí usar sqlite debido a que este proyecto en si no es grande y al ser una prueba pienso que no requiere un servidor de postgresql

## Una decision de arquitectura que tomé de manera independiente

* Decidí hacer una arquitectura monorepo porque ya he trabajado esta arquitectura para proyectos pequeños como este, esta arquitectura facilita cambios coordinados entre frontend y backend, podemos hacer CI/CD centralizado versionamiento conjunto entre otros

## Reflexión
La IA fue útil para acelerar la estructura inicial y revisar alternativas, pero validé las fórmulas, ejecuté pruebas y ajusté el proyecto durante la implementación.