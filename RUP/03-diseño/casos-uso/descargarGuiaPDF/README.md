<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > descargarGuiaPDF() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/README.md)|[Análisis](/RUP/02-analisis/casos-uso/descargarGuiaPDF/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/descargarGuiaPDF/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`descargarGuiaPDF()`](/RUP/02-analisis/casos-uso/descargarGuiaPDF/README.md): `GET /api/v1/guias/{guia_id}/pdf`, compartido entre `Admin` y `Profesor` sin herencia (mismo criterio que `abrirGuia()`). Único caso de esta rebanada de 12 con `alt` real -- traduce el `<<choice>>` de Análisis a `200 OK` o `409 Conflict` según `Guia.tiene_pdf_generado()`. En la rama `200`, el cuerpo es el render real de la plantilla de guía docente (v1, discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)) -- deja de ser el placeholder de bytes fijos. El almacenamiento persistente del PDF sigue fuera de alcance (D3 de #218: re-render desde la fila `Guia` en cada descarga, sin guardar bytes); el lote real de generación en masa pertenece a `generarGuiasPDF()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/descargarGuiaPDF/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DescargarGuiaPDFView` (React) -- pide `GET /api/v1/guias/{guia_id}/pdf`; en la rama roja presenta el mensaje de bloqueo.
- **API**: `routers/guia.py::descargar_guia_pdf(guia_id)` -- aplica el `alt`; en la rama verde llama al módulo de render y devuelve `Response(media_type="application/pdf")`, en la roja `409`.
- **Render**: `app/render/guia_docente.py::render_pdf(guia)` -- módulo nuevo; Jinja2 (`templates/guia_docente.html`) + WeasyPrint. **No** es una capa Service: es presentación adyacente a la I/O, no lógica de negocio (ver Decisiones de diseño).
- **Modelo**: `Guia.tiene_pdf_generado()` -- responde a partir de si `fecha_generacion_pdf` está vacía. El render navega la `Guia` y su cascada (`asignatura_grado.materia.grado.facultad`, `asignatura_grado.requisitos_previos` en vivo -- texto plano, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259), `asignatura_grado.resultados_aprendizaje` en vivo, `asignatura_grado.metodologias_docentes`, `ponderaciones`/`referencias` vinculadas) sin métodos nuevos.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` -- con eager loading de la cascada que el render necesita.

## Decisiones de diseño

- **`Response(media_type="application/pdf")` con bytes de render, no `FileResponse` desde disco**: no hay archivo físico. El PDF se re-renderiza desde la fila `Guia` en cada descarga (D3 de la discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)) -- de facto inmutable (los datos están materializados en la fila y editar una `Guia` `Aprobada` la tira a `Borrador`). El almacenamiento persistente y la generación en lote pertenecen a `generarGuiasPDF()`, no construido aún.
- **Motor: WeasyPrint (Jinja2 + CSS Paged Media), no Chromium ni ReportLab** (D2 de #218). Python puro, sin dependencia de un navegador headless (+300 MB de imagen). Requiere paquetes de sistema (pango/harfbuzz/ffi + fuentes) en el `backend/Dockerfile` -- ver Desarrollo.
- **`app/render/guia_docente.py` es un módulo de presentación/render, no una capa Service**: pyCelda mantiene Fat Model sin Service (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)). Esto no lo debilita -- el módulo no contiene reglas de negocio (no valida, no decide transiciones, no persiste), solo transforma una `Guia` ya cargada en un documento. Es I/O de salida, del mismo tipo que serializar a JSON con Pydantic. No es precedente para introducir Services.
- **Una plantilla, dos salidas** (D4 de #218): `templates/guia_docente.html` sirve tanto el PDF (vía WeasyPrint) como la vista HTML de [`previsualizarGuia()`](/RUP/03-diseño/casos-uso/previsualizarGuia/README.md).
- **Color del render en los diagramas consolidados**: en Análisis, `RenderizadorGuiaDocente` es `#F2AC4E` (Modelo -- clase agnóstica de tecnología que produce el documento); en Diseño, `RenderGuiaDocente` es `#b5bd68` (módulo de funciones `render/guia_docente.py`, como los `routers/`). Es el mismo salto de capa que hace `GuiaController` (Análisis) -> `routers/guia.py` (Diseño), no un error de leyenda.
- **El profesorado del render lee `guia.profesorado` (la copia), sin cambio con #254**: `_contexto()` de `render/guia_docente.py` **no se toca** por el issue [#254](https://github.com/mmasias/pyCelda/issues/254). Las vistas de gestión (`abrir_guia`, `listar_guias_del_grado`) pasan a leer la plantilla en vivo; el render del PDF sigue con la copia congelada -- es el registro oficial de la última aprobación, y `descargarGuiaPDF()` solo sirve guías `Aprobada`, donde `Guia.aprobar()` acaba de sincronizar la copia con la plantilla.
- **`409 Conflict`, no `404`**: el recurso `Guia` existe, lo que falta es una precondición de estado (PDF no generado) -- mismo criterio que `enviarGuiaARevision()` para "pendientes sin guardar".
- **Salvaguarda estructural sin pantalla de bloqueo real**: el botón `[Descargar PDF]` del frontend se ofrece condicionalmente, así que la rama roja del backend es defensiva (llamadas directas a la API), no un camino que la UI dispare.
- **Maquetación v2 (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: `templates/guia_docente.html` se alinea al formulario oficial en blanco `Plantilla-GuiaDocente.pdf` (paged media: cabecera corrida con logo, pie "Página X de Y", secciones numeradas, celdas de etiqueta en azul saturado). El flag `no_oficial` de `render_pdf` deja de ser `False` fijo y pasa a `guia.estado != "Aprobada"` -> marca de agua diagonal en todas las páginas (en la práctica siempre `False` en este camino por el `alt` sobre `tiene_pdf_generado()`, pero correcto por defensa). `_contexto()` agrupa `ReferenciaBibliografica` en 4 subsecciones fijas por mapeo de `tipo`, y pasa `Guia.contenido` como bloque `pre-wrap` en vez de lista de líneas. Sin cambio de participantes ni de secuencia.

## Referencias

- [`descargarGuiaPDF()` en Análisis](/RUP/02-analisis/casos-uso/descargarGuiaPDF/README.md) -- diagrama de colaboración origen, con el `<<choice>>` real y `RenderizadorGuiaDocente`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/README.md).
- [`previsualizarGuia()` en Diseño](/RUP/03-diseño/casos-uso/previsualizarGuia/README.md) -- comparte `app/render/guia_docente.py` (salida HTML, `render_html`).
- [Discussion #218](https://github.com/mmasias/pyCelda/discussions/218) -- D1-D4: artefacto de archivo, motor, semántica de generación, plantilla única.
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial (Frente A); botón `generarGuiaPDF()` para el usuario (Frente B).
- [`editarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- mismo patrón `alt` para un `<<choice>>` de Análisis.
- [`editarSemestreGuia()` en Diseño](/RUP/03-diseño/casos-uso/editarSemestreGuia/README.md) -- quien regenera `fecha_generacion_pdf` cuando aplica.
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- mismo criterio de caso de uso compartido sin herencia entre `Admin` y `Profesor`.
