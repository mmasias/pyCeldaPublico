<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearGrado() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearGrado/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearGrado/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado** (backend + frontend)

**Retocado (issue #148, 2026-09-05)**: `codigo` duplicado ahora rechaza con 409 -- antes no había ninguna restricción, ni de esquema ni de aplicación.

## Código

- **Router**: [`routers/grado.py`](/backend/app/routers/grado.py) -- `crear_grado(facultad_id, datos)`, namespace `/api/v1/admin/facultades/{facultad_id}/grados` (separado de `/api/v1/grados`, variante `DirectorGrado`); comprueba `GradoRepository.obtener_por_codigo(codigo)` antes de crear, 409 si ya existe.
- **Repositorio**: [`repositories/grado.py`](/backend/app/repositories/grado.py) -- `crear(codigo, nombre, facultad_id)`, `obtener_por_codigo(codigo)` (issue #148)
- **Modelo**: [`models/grado.py`](/backend/app/models/grado.py) -- `codigo` con `unique=True` (issue #148)
- **Schema**: [`schemas/grado.py`](/backend/app/schemas/grado.py) -- `GradoCreate`
- **Script de migración**: [`scripts/migrar_unique_codigo_grado.py`](/backend/app/scripts/migrar_unique_codigo_grado.py) (issue #148) -- `plan`/`apply`, crea el índice único `ix_grados_codigo`; aborta sin tocar nada si encuentra `codigo` duplicados sin resolver.
- **Tests**: [`tests/test_grado_admin.py`](/backend/tests/test_grado_admin.py), [`tests/test_migrar_unique_codigo_grado.py`](/backend/tests/test_migrar_unique_codigo_grado.py) (issue #148), [`tests/test_auth_admin.py`](/backend/tests/test_auth_admin.py)
- **Frontend**: [`pages/CrearGradoAdmin.tsx`](/frontend/src/pages/CrearGradoAdmin.tsx) (ruta `/facultades/:facultadId/grados/crear`), botón "+ Crear Grado" en [`Facultad.tsx`](/frontend/src/pages/Facultad.tsx) -- sin cambio: ya propaga cualquier `detail` de error del backend a pantalla (`ApiError.message`), el 409 se muestra sin tocar código.

  Nota (2026-08-30): el botón vivía en `GradosAdmin.tsx`, fusionado con `Facultad.tsx` (discussion #149).

## Contrato de endpoint

### POST `/api/v1/admin/facultades/{facultad_id}/grados`

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
{ "detail": "Ya existe un Grado con código 'GIOI'" }
```

## Listado propio de Admin, anidado bajo Facultad

`GET /api/v1/admin/facultades/{facultad_id}/grados` (`listar_grados_de_la_facultad(facultad_id)` -> `GradoRepository.listar_de_la_facultad(facultad_id)`, con filtro `WHERE facultad_id`) es la variante `Admin` de `abrirGrados()` que antes quedó fuera de alcance (solo existía la variante `DirectorGrado`, filtrada) -- ahora hace falta como punto de entrada real a `crearGrado()`/`eliminarGrado()`. Corregido tras revisión en vivo de Manuel: el listado global sin filtro de PR #120 quedaba huérfano de `Facultad` -- ver Diseño de [`abrirGrados()`](/RUP/03-diseño/casos-uso/abrirGrados/README.md).

## Referencias

- [`crearGrado()` en Diseño](/RUP/03-diseño/casos-uso/crearGrado/README.md) -- secuencia completa, decisión del namespace `/api/v1/admin/facultades/{facultad_id}/grados`.
