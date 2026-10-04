<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > previsualizarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/previsualizarGuia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`previsualizarGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/README.md): el `Profesor` (o el `DirectorPrograma` que dirige el programa, o un `Admin` sobre cualquier guía -- issue [#262](https://github.com/mmasias/pyCelda/issues/262)) ve la `Guia` abierta renderizada con el formato de la guía docente oficial, disponible sin condición de `estado`. Sin `<<choice>>`: la previsualización se sirve en cualquier estado, y el aviso de borrador no oficial (cuando la `Guia` no está `Aprobada`) es presentación condicional dentro de la rama de éxito, no una bifurcación de validación. Sin `HistorialCambio` ni persistencia -- es solo lectura.

El documento se produce con `RenderizadorGuiaDocente`, la misma clase de modelo que usa [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) en su rama verde -- una plantilla, dos formatos de salida (HTML aquí, PDF allí).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/previsualizarGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `PrevisualizarGuiaView`

**Responsabilidades:**
- recoge la solicitud de previsualización sobre la `Guia` abierta.
- presenta la `Guia` renderizada con el formato oficial; añade la banda de aviso de borrador no oficial cuando la `Guia` no está `Aprobada`.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor`/`DirectorPrograma` solicita previsualizar la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIA_ABIERTO` -- self-loop.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- recupera la `Guia` (`previsualizarGuia(guiaId)`), decide a partir de su `estado` si la previsualización es no oficial (`estado != Aprobada`), y pide a `RenderizadorGuiaDocente` el documento HTML.
- no valida ni registra `HistorialCambio` -- la especificación no modela ninguna de las dos cosas.

**Colaboraciones:**
- **Entrada:** `PrevisualizarGuiaView`.
- **Salida:** `Guia`, `GuiaRepository`, `RenderizadorGuiaDocente`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- expone su `estado` y su cascada (`AsignaturaPrograma`, `Materia`, `Programa`, `Facultad`, `Guia.semestre`, `Guia.profesorado`, `Guia.contenido`, `PonderacionEvaluacion`/`ReferenciaBibliografica` vinculadas) para el render.

**Colaboraciones:**
- **Entrada:** `GuiaController`, vía `GuiaRepository`; `RenderizadorGuiaDocente` la navega.

### `GuiaRepository`

**Responsabilidades:**
- recupera la `Guia` por identificador (`obtener(guiaId)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

### `RenderizadorGuiaDocente`

**Responsabilidades:**
- produce el documento de la guía docente en formato HTML (`renderizarHTML(guia, noOficial)`) a partir de la `Guia` y su cascada: datos generales, `Guia.contenido`, `AsignaturaPrograma.requisitosPrevios` (texto plano leído en vivo, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)), `ResultadoAprendizaje` leídos en vivo de `AsignaturaPrograma`, `MetodologiaDocente` de `AsignaturaPrograma`, `PonderacionEvaluacion` vinculadas, `ReferenciaBibliografica` vinculadas; incluye la banda de aviso cuando `noOficial` es verdadero.
- misma plantilla que la salida PDF de [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md).
- **v2 (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: la plantilla se maqueta al formulario oficial en blanco; las `ReferenciaBibliografica` vinculadas se agrupan en 4 subsecciones fijas por mapeo de su `tipo`. En la salida HTML, `noOficial` sigue rindiéndose como banda de aviso al principio del documento (la vista no es paginada); la marca de agua diagonal es exclusiva del PDF de `descargarGuiaPDF()`.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** navega la `Guia` y su cascada (sin repositorios propios: son referencias secundarias).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/wireframes.puml) -- fuente de verdad del render de solo lectura y del aviso condicional.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : previsualizarGuia()`.
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- comparte `RenderizadorGuiaDocente`; salida PDF en vez de HTML, con `<<choice>>` sobre `fechaGeneracionPDF`.
- [`abrirGuia()`](../abrirGuia/README.md) -- autorización de `Profesor` autor / `DirectorPrograma` del programa; `previsualizarGuia()` la amplía con `Admin` (cualquier guía), gemelo de `descargarGuiaPDF()` -- issue [#262](https://github.com/mmasias/pyCelda/issues/262).
- [Discussion #218](https://github.com/mmasias/pyCelda/discussions/218) -- P4 (vista en cualquier estado, aviso), D4 (plantilla única).
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial, bibliografía en 4 subsecciones fijas; la vista HTML conserva la banda de aviso (no paginada).
