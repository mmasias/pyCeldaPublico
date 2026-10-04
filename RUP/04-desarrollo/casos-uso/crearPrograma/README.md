<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPrograma() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado** (backend + frontend)

**Retocado (issue #148, 2026-09-05)**: `codigo` duplicado ahora rechaza con 409 -- antes no había ninguna restricción, ni de esquema ni de aplicación.

## Código

- **Router**: [`routers/programa.py`](/backend/app/routers/programa.py) -- `crear_programa(facultad_id, datos)`, namespace `/api/v1/admin/facultades/{facultad_id}/programas` (separado de `/api/v1/programas`, variante `DirectorPrograma`); comprueba `ProgramaRepository.obtener_por_codigo(codigo)` antes de crear, 409 si ya existe.
- **Repositorio**: [`repositories/programa.py`](/backend/app/repositories/programa.py) -- `crear(codigo, nombre, facultad_id)`, `obtener_por_codigo(codigo)` (issue #148)
- **Modelo**: [`models/programa.py`](/backend/app/models/programa.py) -- `codigo` con `unique=True` (issue #148)
- **Schema**: [`schemas/programa.py`](/backend/app/schemas/programa.py) -- `ProgramaCreate`
- **Script de migración**: [`scripts/migrar_unique_codigo_programa.py`](/backend/app/scripts/migrar_unique_codigo_programa.py) (issue #148) -- `plan`/`apply`, crea el índice único `ix_programas_codigo`; aborta sin tocar nada si encuentra `codigo` duplicados sin resolver.
- **Tests**: [`tests/test_programa_admin.py`](/backend/tests/test_programa_admin.py), [`tests/test_migrar_unique_codigo_programa.py`](/backend/tests/test_migrar_unique_codigo_programa.py) (issue #148), [`tests/test_auth_admin.py`](/backend/tests/test_auth_admin.py)
- **Frontend**: [`pages/CrearProgramaAdmin.tsx`](/frontend/src/pages/CrearProgramaAdmin.tsx) (ruta `/facultades/:facultadId/programas/crear`), botón "+ Crear Programa" en [`Facultad.tsx`](/frontend/src/pages/Facultad.tsx) -- sin cambio: ya propaga cualquier `detail` de error del backend a pantalla (`ApiError.message`), el 409 se muestra sin tocar código.

  Nota (2026-08-30): el botón vivía en `ProgramasAdmin.tsx`, fusionado con `Facultad.tsx` (discussion #149).

## Contrato de endpoint

### POST `/api/v1/admin/facultades/{facultad_id}/programas`

Requiere `Depends(require_admin)`. `codigo`+`nombre` obligatorios (a diferencia de `crearAsignatura()`/`crearUniversidad()`, que solo pedían un campo). `facultad_id` viaja en la URL, no en el body (mismo patrón que `POST /api/v1/universidades/{universidad_id}/facultades`).

**Request:**
```json
{ "codigo": "GII", "nombre": "Grado en Ingeniería Informática" }
```

**Response (201 Created):**
```json
{ "id": 1, "codigo": "GII", "nombre": "Grado en Ingeniería Informática", "estado": "Vigente", "facultad_id": 1 }
```

**Response (409 Conflict, issue #148):**
```json
{ "detail": "Ya existe un Programa con código 'GIOI'" }
```

## Listado propio de Admin, anidado bajo Facultad

`GET /api/v1/admin/facultades/{facultad_id}/programas` (`listar_programas_de_la_facultad(facultad_id)` -> `ProgramaRepository.listar_de_la_facultad(facultad_id)`, con filtro `WHERE facultad_id`) es la variante `Admin` de `abrirProgramas()` que antes quedó fuera de alcance (solo existía la variante `DirectorPrograma`, filtrada) -- ahora hace falta como punto de entrada real a `crearPrograma()`/`eliminarPrograma()`. Corregido tras revisión en vivo de Manuel: el listado global sin filtro de PR #120 quedaba huérfano de `Facultad` -- ver Diseño de [`abrirProgramas()`](/RUP/03-diseño/casos-uso/abrirProgramas/README.md).

## Referencias

- [`crearPrograma()` en Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md) -- secuencia completa, decisión del namespace `/api/v1/admin/facultades/{facultad_id}/programas`.
