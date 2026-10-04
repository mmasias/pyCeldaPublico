<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md): CRUD real e inmediato contra `MetodologiaDocenteRepository`. Ambos campos obligatorios (`codigo`, `descripcion`) y sin `<<choice>>` -- Requisitos cierra explícitamente "sin patrón C->U": los dos datos identifican la metodología desde el alta, no hay un dato secundario que diferir a la edición (a diferencia de `crearAsignatura()`, que solo pide `nombre`). La salida es única, sin rama de rechazo, a `:METODOLOGIA_DOCENTE_ABIERTO` -- la transición lleva la nota `editarMetodologiaDocente()` como edición disponible desde el detalle alcanzado, no como `<<include>>` C->U.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearMetodologiaDocenteView`

**Responsabilidades:**
- presenta el formulario de creación: `codigo` y `descripcion`, ambos obligatorios.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO` -- el `Admin` solicita crear una `MetodologiaDocente` desde el listado.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIA_DOCENTE_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- valida que `codigo` y `descripcion` estén presentes (`validarDatosObligatorios(codigo, descripcion)`).
- crea la `MetodologiaDocente` directamente en `MetodologiaDocenteRepository`, real e inmediato (`crearMetodologiaDocente(codigo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `CrearMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion` desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- crea la `MetodologiaDocente` (`crear(codigo, descripcion)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/wireframes.puml) -- fuente de verdad del formulario, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : crearMetodologiaDocente()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente { codigo, descripcion }`, catálogo institucional.
- [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md) -- edición disponible desde el detalle alcanzado tras crear.
- [`crearAsignatura()`](../crearAsignatura/README.md) -- contraste: creación con patrón C->U (solo `nombre` en el alta).
