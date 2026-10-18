<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`crearActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): formulario de `codigo` y `nombre`, sin patrón C→U, como [`crearCompetencia()`](../crearCompetencia/README.md). El `<<choice>>` de código repetido lo resuelve el controlador contra el repositorio antes de escribir: si el código ya lo usa otra actividad formativa del `Programa`, el formulario sigue con lo escrito y el mensaje. La actividad nace siempre dentro de un `Programa` (`programaId`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearActividadFormativaView`

**Responsabilidades:**
- presenta el formulario: `codigo` y `nombre`, los dos obligatorios.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO`.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDAD_FORMATIVA_ABIERTO` (ficha de la creada, desde la que se edita).

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- valida que el `codigo` no lo use otra actividad formativa del `Programa`.
- crea la `ActividadFormativa`, real e inmediata.

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
- responde si un `codigo` está en uso en el `Programa` (`codigoEnUso(programaId, codigo)`).
- crea la `ActividadFormativa` (`crear(programaId, codigo, nombre)`). Al crearla puebla a 0 las filas de asociación de las `Materia`/`AsignaturaPrograma` ya existentes de ese `Programa` (invariante de autopoblado): efecto de persistencia, sin colaboración nueva de análisis.

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa` y sus dos clases de asociación (`ActividadFormativaMateria`, `ActividadFormativaAsignaturaPrograma`).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/wireframes.puml) -- fuente de verdad.
- [`crearCompetencia()`](../crearCompetencia/README.md) -- patrón de origen.
- [`editarActividadFormativa()`](../editarActividadFormativa/README.md) -- edición disponible desde la ficha alcanzada tras crear.
