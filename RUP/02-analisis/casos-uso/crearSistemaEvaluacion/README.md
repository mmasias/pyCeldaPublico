<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearSistemaEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/README.md): CRUD real e inmediato contra `SistemaEvaluacionRepository` -- los cuatro campos (`tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`) se piden de una vez en el alta, sin patrón C->U. `descripcion` es opcional (default `""`, mismo patrón que `MetodologiaMateria.descripcionPropia`); `tipo`, `ponderacionMinima` y `ponderacionMaxima` son obligatorios. La coherencia del rango (`0 <= ponderacionMinima <= ponderacionMaxima <= 100`) es validación de forma de la Vista, no una regla de negocio del controlador -- Requisitos no documenta ninguna invariante adicional y el backend no la exige. La salida es única, sin rama de rechazo, a `:SISTEMA_EVALUACION_ABIERTO` -- la transición lleva la nota `editarSistemaEvaluacion()` como edición disponible desde el detalle alcanzado, no como `<<include>>` C->U (mismo criterio que `crearMetodologiaDocente()`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearSistemaEvaluacionView`

**Responsabilidades:**
- presenta el formulario de creación: `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima` -- `tipo` selector de lista fija (`"Evaluación continua"`/`"Evaluación final"`, issue [#14](https://github.com/mmasias/pyCelda/issues/14)), `descripcion` opcional, `tipo`/`ponderacionMinima`/`ponderacionMaxima` obligatorios según el wireframe.
- valida la coherencia del rango `0 <= mínima <= máxima <= 100` antes de solicitar crear (validación de forma, no de negocio).
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:SISTEMAS_EVALUACION_ABIERTO` -- el `Admin` solicita crear un `SistemaEvaluacion` de la `Materia`.
- **Control:** `SistemaEvaluacionController`.
- **Salida:** `:SISTEMA_EVALUACION_ABIERTO`.

## Clases de controlador

### `SistemaEvaluacionController`

**Responsabilidades:**
- valida que `tipo`, `ponderacionMinima` y `ponderacionMaxima` estén presentes (`validarDatosObligatorios(tipo, ponderacionMinima, ponderacionMaxima)`).
- crea el `SistemaEvaluacion` directamente en `SistemaEvaluacionRepository`, real e inmediato (`crearSistemaEvaluacion(materiaId, tipo, descripcion, ponderacionMinima, ponderacionMaxima)`).

**Colaboraciones:**
- **Entrada:** `CrearSistemaEvaluacionView`.
- **Salida:** `SistemaEvaluacionRepository`.

## Clases de modelo

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima` desde el momento de crearse, ligado a su `Materia` por composición.

**Colaboraciones:**
- **Entrada:** creado por `SistemaEvaluacionRepository`.

### `SistemaEvaluacionRepository`

**Responsabilidades:**
- crea el `SistemaEvaluacion` bajo la `Materia` (`crear(materiaId, tipo, descripcion, ponderacionMinima, ponderacionMaxima)`) -- persistencia real e inmediata.

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** gestiona `SistemaEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/wireframes.puml) -- fuente de verdad del formulario, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : crearSistemaEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia *-- SistemaEvaluacion`.
- [`editarSistemaEvaluacion()`](../editarSistemaEvaluacion/README.md) -- edición disponible desde el detalle alcanzado tras crear.
- [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md) -- mismo patrón de alta sin C->U y nota de edición disponible en la salida.
