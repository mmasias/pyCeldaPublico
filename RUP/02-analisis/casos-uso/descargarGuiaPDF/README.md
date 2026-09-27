<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > descargarGuiaPDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/descargarGuiaPDF/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`descargarGuiaPDF()`](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/README.md): compartido entre `Admin`, `Profesor` y `DirectorGrado` (heredado) sin relación de herencia entre los dos primeros, mismo criterio que [`abrirGuia()`](../abrirGuia/README.md). Único caso de esta rebanada con `<<choice>>` real: si `Guia.fechaGeneracionPDF` está vacía, bloquea con mensaje; si no, presenta el PDF. El README de Requisitos ya señala que esta rama roja es una salvaguarda estructural que la interfaz nunca dispara (el botón `[Descargar PDF]` se ofrece condicionalmente), pero la especificación la modela igual -- y la regla de cobertura de Análisis exige representarla.

En la rama verde, el PDF que se presenta es el render de la plantilla oficial de guía docente a partir de la `Guia` y su cascada (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)) -- responsabilidad de una clase de modelo nueva, `RenderizadorGuiaDocente`, compartida con [`previsualizarGuia()`](../previsualizarGuia/README.md) (misma plantilla, dos salidas). Antes de este retoque la rama verde solo presentaba un binario placeholder.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/descargarGuiaPDF/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DescargarGuiaPDFView`

**Responsabilidades:**
- recoge la solicitud de descarga sobre la `Guia` abierta.
- en la rama verde, presenta el PDF.
- en la rama roja, presenta el mensaje de bloqueo "PDF no generado todavía" -- salvaguarda estructural, no alcanzable desde el botón condicional de la interfaz.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Admin`/`Profesor` solicita descargar el PDF de la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIA_ABIERTO` en ambos casos -- self-loop, con "presenta el PDF" (verde) o "PDF no generado todavía" (rojo).

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- recupera la `Guia` y aplica el `<<choice>>`: pregunta si tiene PDF generado (`descargarPDF(guiaId)`) y devuelve el resultado a la Vista, que decide la rama.
- en la rama verde, pide a `RenderizadorGuiaDocente` el documento PDF de la `Guia`.

**Colaboraciones:**
- **Entrada:** `DescargarGuiaPDFView`.
- **Salida:** `Guia`, `GuiaRepository`, `RenderizadorGuiaDocente`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- responde si tiene su PDF generado (`tienePDFGenerado()`), a partir de si `fechaGeneracionPDF` está vacía.

**Colaboraciones:**
- **Entrada:** `GuiaController`, vía `GuiaRepository`.

### `RenderizadorGuiaDocente`

**Responsabilidades:**
- produce el documento de la guía docente en formato PDF (`renderizarPDF(guia)`) a partir de la `Guia` y su cascada: datos generales (`AsignaturaGrado`, `Materia`, `Grado`, `Facultad`, `Guia.semestre`, `Guia.profesorado`), `Guia.contenido`, `AsignaturaGrado.requisitosPrevios` (texto plano leído en vivo, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)), `ResultadoAprendizaje` leídos en vivo de `AsignaturaGrado`, `MetodologiaDocente` de `AsignaturaGrado`, `PonderacionEvaluacion` vinculadas, `ReferenciaBibliografica` vinculadas.
- misma plantilla que la salida HTML de [`previsualizarGuia()`](../previsualizarGuia/README.md) -- una plantilla, dos formatos de salida.
- **v2 (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: la plantilla se maqueta al formulario oficial en blanco (`docs/PROPUESTA_PLANTILLA/`); las `ReferenciaBibliografica` vinculadas se agrupan en 4 subsecciones fijas (básica / complementaria / webs / otras fuentes) por mapeo de su `tipo`, en vez de una subsección libre por valor de `tipo`; y el indicador de guía no oficial (`estado != Aprobada`) se rinde como marca de agua diagonal en todas las páginas del PDF (en la salida HTML de `previsualizarGuia()` sigue siendo la banda de aviso). Sin clase nueva ni cambio de flujo.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** navega la `Guia` y su cascada (sin repositorios propios: son referencias secundarias, mismo criterio que `crearPonderacionEvaluacion()` con `Materia`).

### `GuiaRepository`

**Responsabilidades:**
- recupera la `Guia` por identificador (`obtener(guiaId)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/wireframes.puml) -- fuente de verdad del `<<choice>>` y de por qué la interfaz no dispara la rama roja.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : descargarGuiaPDF()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia{fechaGeneracionPDF}`.
- [`editarSemestreGuia()`](../editarSemestreGuia/README.md) -- quien regenera `fechaGeneracionPDF` cuando aplica.
- [`abrirGuia()`](../abrirGuia/README.md) -- mismo criterio de caso de uso compartido sin herencia entre `Admin` y `Profesor`.
- [`previsualizarGuia()`](../previsualizarGuia/README.md) -- comparte `RenderizadorGuiaDocente` (misma plantilla, salida HTML en vez de PDF).
- [Discussion #218](https://github.com/mmasias/pyCelda/discussions/218) -- motor de render del v1, plantilla única para PDF y HTML.
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial, bibliografía en 4 subsecciones fijas, marca de agua diagonal en el PDF no oficial.
