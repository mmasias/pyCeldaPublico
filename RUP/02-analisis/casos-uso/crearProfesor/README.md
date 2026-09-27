<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearProfesor/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearProfesor()`](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/README.md): CRUD real e inmediato contra `ProfesorRepository`. Ambos campos obligatorios (`nombre`, `email`) y sin `<<choice>>` -- Requisitos cierra explícitamente que este es el único caso del lote sin patrón C->U: los dos atributos de `Profesor` son necesarios para que el alta tenga sentido, no hay nada que diferir a la edición. La salida es única, sin rama de rechazo, a `:PROFESOR_ABIERTO` -- la transición lleva la nota `editarProfesor()` como edición disponible desde el detalle alcanzado, no como `<<include>>` C->U.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearProfesor/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearProfesorView`

**Responsabilidades:**
- presenta el formulario de creación: `nombre` y `email`, ambos obligatorios.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:PROFESORES_ABIERTO` -- el `Admin` solicita crear un `Profesor` desde el listado.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO`.

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- valida que `nombre` y `email` estén presentes (`validarDatosObligatorios(nombre, email)`).
- crea el `Profesor` directamente en `ProfesorRepository`, real e inmediato (`crearProfesor(nombre, email)`).

**Colaboraciones:**
- **Entrada:** `CrearProfesorView`.
- **Salida:** `ProfesorRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email` desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- crea el `Profesor` (`crear(nombre, email)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `Profesor`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/wireframes.puml) -- fuente de verdad del formulario, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESOR_ABIERTO : crearProfesor()`.
- [`editarProfesor()`](../editarProfesor/README.md) -- edición disponible desde el detalle alcanzado tras crear.
- [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md) -- mismo patrón de alta sin C->U con ambos campos en el formulario.
