<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md): CRUD real e inmediato contra `ActividadFormativaRepository`. Ambos campos obligatorios (`codigo`, `nombre`) y sin `<<choice>>` -- sin patrón C->U, igual que `crearMetodologiaDocente()`: los dos datos identifican la actividad desde el alta. La salida es única, sin rama de rechazo, a `:ACTIVIDAD_FORMATIVA_ABIERTO` -- la transición lleva la nota `editarActividadFormativa()` como edición disponible desde el detalle alcanzado, no como `<<include>>` C->U. La `ActividadFormativa` se crea siempre dentro de una `Universidad` (`universidadId`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearActividadFormativaView`

**Responsabilidades:**
- presenta el formulario de creación: `codigo` y `nombre`, ambos obligatorios.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` -- el `Admin` solicita crear una `ActividadFormativa` desde el listado.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDAD_FORMATIVA_ABIERTO`.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- valida que `codigo` y `nombre` estén presentes (`validarDatosObligatorios(codigo, nombre)`).
- crea la `ActividadFormativa` directamente en `ActividadFormativaRepository`, real e inmediato (`crearActividadFormativa(universidadId, codigo, nombre)`).

**Colaboraciones:**
- **Entrada:** `CrearActividadFormativaView`.
- **Salida:** `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- porta `codigo` y `nombre` desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `ActividadFormativaRepository`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- crea la `ActividadFormativa` (`crear(universidadId, codigo, nombre)`) -- persistencia real e inmediata, no una mutación de sesión. Al crearla puebla a 0 las filas de asociación de las `Materia`/`AsignaturaPrograma` ya existentes de esa `Universidad` (invariante de autopoblado, issue [#655](https://github.com/mmasias/pyCelda/issues/655)): efecto de persistencia, sin colaboración nueva de análisis.

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/wireframes.puml) -- fuente de verdad de el formulario y la salida única sin rama de rechazo..
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : crearActividadFormativa()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo de `Universidad` (`Universidad *-- ActividadFormativa`).
- [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md) -- clúster plantilla.
- [`editarActividadFormativa()`](../editarActividadFormativa/README.md) -- edición disponible desde el detalle alcanzado tras crear.
- [`crearAsignatura()`](../crearAsignatura/README.md) -- contraste: creación con patrón C->U.
