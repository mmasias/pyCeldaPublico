<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Configuración y estructura del proyecto

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Estructura de directorios y decisiones técnicas transversales necesarias para materializar en código los 9 `secuencia.puml` de la rebanada, a nivel de fase (no por caso de uso). Se escribe ahora porque la condición que aplazaba este documento -- "cuando haya más de un caso de uso construido y las decisiones transversales dejen de ser hipotéticas" (`RUP/03-diseño/README.md`) -- ya se cumple con los 9 casos cerrados.

Adaptado del precedente de [pySigHor](https://github.com/mmasias/pySigHor/blob/diseño-fastapi-react/RUP/02-diseño/configuracion-proyecto.md), **sin copiarlo literal**: ese documento trae `backend/app/services/`, capa que pyCelda ya rechazó (Fat Model, discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)), y detalla frontend/JWT/migraciones -- piezas fuera del alcance de esta rebanada (UI explícitamente fuera de esta fase, autenticación stub, sin login real).

## Estructura de directorios

```
backend/app/
├── models/          # SQLAlchemy, Fat Model (Guia.aprobar(), Guia.sincronizar_ponderaciones(), ...)
├── schemas/         # Pydantic (request/response de cada endpoint)
├── repositories/    # CRUD puro, sin lógica de negocio
├── routers/         # funciones sueltas decoradas, sin capa Service
├── render/          # presentación de salida: guia_docente.py (Jinja2 + WeasyPrint), no es capa Service
├── templates/       # guia_docente.html -- una plantilla, dos salidas (PDF y vista HTML)
├── static/          # UNEATLANTICO_logo.svg (images/ no viaja en la imagen Docker, #202)
└── core/            # configuración, login real con Google OAuth2/OIDC

frontend/
├── index.html
├── src/
│   ├── main.tsx     # entrypoint, BrowserRouter
│   ├── App.tsx       # rutas: "/" (Login), "/guia/:id" (AbrirGuia)
│   ├── api.ts        # API_BASE, tipos de respuesta, fetch con credentials: "include"
│   └── pages/
│       ├── Login.tsx      # redirige a GET /auth/login
│       └── AbrirGuia.tsx  # GET /api/v1/guias/{id}
├── vite.config.ts
├── tsconfig.json
└── package.json
```

**Sin `services/`**: el Router llama directamente a `repositories/` y a los métodos de `models/` -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58), verificada contra código real de pySigHor (`backend/app/services/aula_service.py`, modelo anémico que `docs/2Think/MVCHowTo.md` rechaza citando a Fowler). `render/guia_docente.py` (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)) **no** reabre esa decisión: es presentación de salida -- transforma una `Guia` ya cargada en un documento PDF/HTML, sin validar, decidir transiciones ni persistir -- del mismo tipo que serializar a JSON con Pydantic, no una capa de negocio.

**`routers/` es funcional, no orientado a objetos**: cada módulo es un fichero de funciones sueltas decoradas con `@router.get`/`@router.post`/etc., nunca una clase `*Controller` -- confirmado contra `backend/app/routers/aulas.py` de pySigHor y contra los 9 `README.md` de esta rebanada, que citan `routers/guia.py`, `routers/ponderacion_evaluacion.py`, `routers/referencia_bibliografica.py` como módulos, nunca como clases. Ver el diagrama de clases de esta misma fase para el inventario completo de funciones por módulo.

**Frontend: UI mínima de prueba, no la rebanada completa de 9 pantallas**: los 9 `secuencia.puml` modelan la Vista como participante genérico "Vista (React)" sin comprometerse con una estructura de carpetas (ver `RUP/02-analisis/README.md`, discussion [#57](https://github.com/mmasias/pyCelda/discussions/57)) -- decisión que sigue en pie para las otras 8 pantallas. Lo que entra en alcance ahora es solo la prueba de fuego del login real (Google OAuth2/OIDC, discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)): `frontend/` con Vite + React + TypeScript, dos pantallas (`Login`, `AbrirGuia`), sin gestor de estado ni capa de servicios propia -- `src/api.ts` centraliza `fetch` con `credentials: "include"` (necesario para que la cookie httpOnly de sesión viaje al backend en `:8000`). `AbrirGuia` sigue el wireframe de `RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/wireframes.puml`, pero solo rellena con datos reales los campos que `AbrirGuiaResponse` devuelve (`estado`, `fecha_ultima_modificacion`, `ponderaciones`, `referencias`) -- las secciones que dependerían de `AsignaturaPrograma` (nombre de asignatura, semestre, resultados de aprendizaje, metodologías), deliberadamente fuera de esta rebanada, se muestran marcadas como "Fuera de alcance de esta rebanada" en vez de inventar datos. Documentar las 8 pantallas restantes sigue siendo trabajo de una rebanada posterior.

## Stack

Ya decidido en conversación, registrado en la discussion [#57](https://github.com/mmasias/pyCelda/discussions/57): **Python + FastAPI + SQLAlchemy + SQLite**.

- **FastAPI**: framework de la capa `routers/` -- funciones async decoradas, validación automática de entrada vía `schemas/` (Pydantic).
- **SQLAlchemy**: ORM de `models/` -- clases `Base`, columnas y relaciones; los métodos de dominio (`Guia.aprobar()`, `SistemaEvaluacion.validar_maximo()`, ...) viven en la propia clase (Fat Model), no en un mixin ni en un service.
- **SQLite**: motor de base de datos -- suficiente para la rebanada mínima (9 casos de uso, sin requisito de concurrencia ni volumen); no se descarta migrar a otro motor cuando el catálogo escale, pero esa decisión no se toma aquí.
- **Jinja2 + WeasyPrint** (v1 del render de la guía docente, discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)): Jinja2 para la plantilla `templates/guia_docente.html`, WeasyPrint (Python puro, CSS Paged Media -- no Chromium headless) para convertirla a PDF en `descargarGuiaPDF()`; la vista HTML de `previsualizarGuia()` sirve la misma plantilla sin pasar por WeasyPrint. WeasyPrint necesita librerías de sistema (`libpango`, `libharfbuzz`, `libffi`, fuentes) en el `backend/Dockerfile` -- `python:3.12-slim` no las trae.
- **Autenticación real, Google OAuth2/OIDC** (discussion [#62](https://github.com/mmasias/pyCelda/discussions/62), sustituye al stub inicial de la decisión 3 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)): "Sign in with Google" vía `Authlib`, restringido al dominio institucional de Workspace (parámetro `hd`), sin auto-registro -- el email de la cuenta tiene que coincidir con un `Profesor`/`DirectorPrograma` ya existente en la base de datos, o el login se rechaza. Sesión vía JWT (`joserfc`) en cookie `httpOnly`, sin almacén de sesión en servidor. Detalle completo en [`RUP/04-desarrollo/README.md`](/RUP/04-desarrollo/README.md#autenticación-real-google-oauth2oidc). `iniciarSesion()` no está en el catálogo de 91 casos de uso de pyCelda como CU propio -- este mecanismo es Diseño/Desarrollo, no Requisitos (ver discussion #62).

## Mapeo entre artefactos de Diseño y código

| Artefacto de Diseño | Módulo/clase Python |
|---|---|
| `Guia` (Modelo) | `backend/app/models/guia.py` |
| `PonderacionEvaluacion` (Modelo) | `backend/app/models/ponderacion_evaluacion.py` |
| `ReferenciaBibliografica` (Modelo) | `backend/app/models/referencia_bibliografica.py` |
| `SistemaEvaluacion` (Modelo) | `backend/app/models/sistema_evaluacion.py` |
| `Materia` (Modelo) | `backend/app/models/materia.py` |
| `HistorialCambio` (Modelo) | `backend/app/models/historial_cambio.py` |
| `ResultadoAprendizaje` (Modelo) | `backend/app/models/resultado_aprendizaje.py` |
| `MetodologiaDocente` (Modelo) | `backend/app/models/metodologia_docente.py` |
| `MetodologiaMateria` (Modelo) | `backend/app/models/metodologia_materia.py` |
| `Programa` (Modelo) | `backend/app/models/programa.py` |
| `AsignaturaPrograma` (Modelo) | `backend/app/models/asignatura_programa.py` |
| `Profesor` (Modelo) | `backend/app/models/profesor.py` |
| `GuiaRepository` | `backend/app/repositories/guia.py` |
| `PonderacionEvaluacionRepository` | `backend/app/repositories/ponderacion_evaluacion.py` |
| `ReferenciaBibliograficaRepository` | `backend/app/repositories/referencia_bibliografica.py` |
| `MateriaRepository` | `backend/app/repositories/materia.py` |
| `SistemaEvaluacionRepository` | `backend/app/repositories/sistema_evaluacion.py` |
| `ResultadoAprendizajeRepository` | `backend/app/repositories/resultado_aprendizaje.py` |
| `MetodologiaDocenteRepository` | `backend/app/repositories/metodologia_docente.py` |
| `MetodologiaMateriaRepository` | `backend/app/repositories/metodologia_materia.py` |
| `AsignaturaProgramaRepository` | `backend/app/repositories/asignatura_programa.py` |
| `ProgramaRepository` | `backend/app/repositories/programa.py` |
| `routers/guia.py` (12 funciones) | `backend/app/routers/guia.py` |
| `render/guia_docente.py` (`render_pdf`, `render_html`) | `backend/app/render/guia_docente.py` |
| `templates/guia_docente.html` | `backend/app/templates/guia_docente.html` |
| `routers/ponderacion_evaluacion.py` (6 funciones) | `backend/app/routers/ponderacion_evaluacion.py` |
| `routers/referencia_bibliografica.py` (4 funciones) | `backend/app/routers/referencia_bibliografica.py` |
| `routers/resultado_aprendizaje.py` (6 funciones) | `backend/app/routers/resultado_aprendizaje.py` |
| `routers/materia.py` (12 funciones) | `backend/app/routers/materia.py` |
| `routers/asignatura_programa.py` (12 funciones) | `backend/app/routers/asignatura_programa.py` |
| `routers/programa.py` (2 funciones) | `backend/app/routers/programa.py` |

Sin fila de Service: no existe esa capa. Sin fila de Vista/frontend: la Vista de los 89 `secuencia.puml` no mapea 1:1 a una clase de Diseño -- `frontend/src/pages/Login.tsx` y `frontend/src/pages/AbrirGuia.tsx` (ver arriba) son las dos únicas pantallas reales hasta ahora, el resto sigue sin construir.

## Variables de entorno

Sin secretos reales comiteados -- ver `backend/.env.example` (plantilla, valores vacíos/de ejemplo) y `backend/.gitignore` (`*.env` fuera del repo).

|Variable|Obligatoria|Descripción|
|-|-|-|
|`GOOGLE_CLIENT_ID`|Sí, para login real|Client ID de la app OAuth registrada en Google Cloud Console.|
|`GOOGLE_CLIENT_SECRET`|Sí, para login real|Client Secret de la misma app. Nunca en texto plano fuera de `.env`.|
|`GOOGLE_HD`|Recomendada|Dominio institucional de Workspace (ej. `uneatlantico.es`) -- restringe el login a ese dominio vía el parámetro `hd`. Vacía = sin restricción (solo para desarrollo local sin cuenta de Workspace a mano).|
|`SESSION_SECRET_KEY`|Sí|Clave de firma HS256 de la cookie de sesión (JWT). Generar con `openssl rand -hex 32`, nunca reusar el valor de ejemplo.|
|`OAUTH_REDIRECT_URI`|No (default `http://localhost:8000/auth/callback`)|Callback registrado en Google Cloud Console. En producción depende del dominio final del despliegue (Tailscale + VPS ya decidido, dominio concreto todavía pendiente) -- actualizar aquí y en la consola de Google a la vez.|
|`FRONTEND_URL`|No (default `http://localhost:5173`)|Origen del frontend -- `routers/auth.py::callback`/`logout` redirigen aquí tras poner/borrar la cookie de sesión. Antes de existir `frontend/`, ambas rutas redirigían a `/` (la propia API, sin esa ruta) -- error real encontrado en la primera prueba end-to-end del login, ver `RUP/04-desarrollo/README.md`.|
|`CURSO_ACADEMICO_VIGENTE`|No (default `2026-2027`)|Año que se imprime en la cabecera de la guía docente renderizada (`descargarGuiaPDF()`/`previsualizarGuia()`, discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)). Constante mientras `CursoAcademico` no esté modelado en el backend -- issue [#222](https://github.com/mmasias/pyCelda/issues/222).|

**Arrancar el backend real requiere `--env-file`**: `uvicorn app.main:app --env-file .env` -- `python -m dotenv`/`load_dotenv()` no se invoca en `core/config.py` (se evaluó y se descartó: contamina el entorno de `pytest` con los valores reales de `.env`, rompiendo el aislamiento de tests). `core/config.py` solo lee `os.environ`; sin `--env-file` (o sin exportar las variables a mano) el proceso ve todas las variables vacías y `/auth/login` falla con `500 Login con Google sin configurar` -- error real encontrado en la primera prueba end-to-end.

## Pendiente

- **Esquemas Pydantic concretos** (`schemas/`) -- cada `secuencia.puml` ya nombra el JSON de entrada/salida de cada endpoint (`PonderacionEvaluacionCreate`, `GuiaResponse`, etc.); la definición campo a campo se escribe junto con el código, no aquí.
- **Callback de producción**: `OAUTH_REDIRECT_URI` y el registro correspondiente en Google Cloud Console dependen del dominio final del despliegue, todavía sin decidir (ver discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)).
- **Login de `Admin`**: `Admin.email` ya está formalizado en `modeloDominio.puml`, pero su login no se prueba hasta que exista la mini-rebanada de `Admin` -- ninguno de los 7 endpoints reales actuales es de `Admin`.

## Referencias

- [`RUP/03-diseño/README.md`](/RUP/03-diseño/README.md) -- criterio de fase, sin capa Service.
- [`RUP/03-diseño/diagrama-clases-diseño.puml`](/RUP/03-diseño/diagrama-clases-diseño.puml) -- inventario completo de clases/módulos y métodos de los 9 casos de uso.
- [`RUP/04-desarrollo/README.md`](/RUP/04-desarrollo/README.md) -- implementación real del login, tests.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño y decisión de no usar capa Service.
- Discussion [#60](https://github.com/mmasias/pyCelda/discussions/60) -- criterio de este documento y del diagrama de clases.
- Discussion [#62](https://github.com/mmasias/pyCelda/discussions/62) -- criterio de login real con Google, `Admin.email`.
- [Configuración y estructura del proyecto de pySigHor](https://github.com/mmasias/pySigHor/blob/diseño-fastapi-react/RUP/02-diseño/configuracion-proyecto.md) -- precedente, no copiado literal (trae `services/`, frontend y JWT completos, fuera de alcance aquí).
