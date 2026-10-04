<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > previsualizarGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/previsualizarGuia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-03
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`previsualizarGuia()`](/RUP/02-analisis/casos-uso/previsualizarGuia/README.md): `GET /api/v1/guias/{guia_id}/vista`, disponible en cualquier estado de la `Guia`. Sin `alt` sobre el estado (a diferencia de [`descargarGuiaPDF()`](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md), que sí tiene `409` si no hay PDF generado): la previsualización se sirve siempre, y el flag `no_oficial` (derivado de `Guia.estado != "Aprobada"`) decide si la plantilla pinta la banda de aviso. El único `alt` es de autorización (`404` uniforme).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/previsualizarGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `PrevisualizarGuiaView` (React) -- pide `GET /api/v1/guias/{guia_id}/vista`; presenta el HTML recibido, con la banda de aviso ya incluida en el propio documento cuando aplica.
- **API**: `routers/guia.py::previsualizar_guia(guia_id)` -- función nueva; resuelve autorización, deriva `no_oficial`, llama al módulo de render y devuelve `HTMLResponse`.
- **Render**: `app/render/guia_docente.py::render_html(guia, no_oficial)` -- módulo nuevo, compartido con `descargarGuiaPDF()`; Jinja2 (`templates/guia_docente.html`), sin pasar por WeasyPrint.
- **Modelo**: `Guia.estado` -- sin métodos nuevos; el render navega la cascada (`asignatura_programa.materia.programa.facultad`, `asignatura_programa.requisitos_previos` en vivo -- texto plano, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259), `asignatura_programa.resultados_aprendizaje` en vivo, `asignatura_programa.metodologias_docentes`, `ponderaciones`/`referencias` vinculadas).
- **Repositorio**: `GuiaRepository.obtener(guia_id)` -- mismo eager loading de la cascada que `descargarGuiaPDF()`.

## Decisiones de diseño

- **`HTMLResponse`, no `Response(application/pdf)`**: misma plantilla `templates/guia_docente.html`, pero servida como HTML directo -- sin el paso de WeasyPrint. Es el camino barato para iterar la maqueta y previsualizar (D1 de la discussion [#218](https://github.com/mmasias/pyCelda/discussions/218): PDF oficial + página HTML subproducto de la misma plantilla).
- **Sin gate de `estado`**: disponible en `Borrador`/`EnRevision`/`Aprobada`/`Rechazada` (P4 de #218). El PDF mantiene su `409`; la previsualización no lo necesita -- su valor es justamente "ver cómo queda antes de enviar".
- **Banda de aviso en la plantilla, no en el router**: `render_html(guia, no_oficial=guia.estado != "Aprobada")`; la plantilla pinta `{% if no_oficial %}` una banda roja de "borrador no oficial". El router solo deriva el booleano.
- **Maquetación v2 (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: la plantilla compartida se alinea al formulario oficial en blanco. La salida HTML **no es paginada**: `no_oficial` se mantiene como banda roja al principio del documento; la cabecera repetida, el pie "Página X de Y" y la marca de agua diagonal son exclusivos del PDF de `descargarGuiaPDF()` (paged media / WeasyPrint). `render_html` no cambia de firma; `_contexto()` gana el agrupado de bibliografía en 4 subsecciones fijas y `Guia.contenido` como bloque `pre-wrap`.
- **Autorización: el mismo gate que `descargarGuiaPDF()`** (issue [#262](https://github.com/mmasias/pyCelda/issues/262), gemelo del [#220](https://github.com/mmasias/pyCelda/issues/220)): `admin_email is not None or _tiene_acceso_a_guia(...)` -- `Admin` previsualiza cualquier guía; `Profesor` que imparte la asignatura **o** `DirectorPrograma` que dirige el programa, con `404` uniforme. El `get_current_rol` que tenía este endpoint (403 si la cuenta no era `Profesor` ni `DirectorPrograma`) bloqueaba justo al `Admin`; se retira. La auth de `Admin` en `routers/guia.py` la construyó [#238](https://github.com/mmasias/pyCelda/issues/238) para `descargar_guia_pdf`; #262 la reutiliza. #218 P3 ya fijaba el modelo "mismo que `descargarGuiaPDF()`"; el v1 dejó a `Admin` diferido (§3/a) solo porque ese plumbing no existía.
- **Ruta `/vista`**: en español, coherente con la convención del proyecto (`/pdf`, `/semestre`, `/borrador`, `/enviar-a-revision`).
- **Año de la cabecera desde una constante de config, no de la `Guia`**: `Settings.curso_academico_vigente` (env var `CURSO_ACADEMICO_VIGENTE`) -- el backend del v1 no modela `CursoAcademico`, así que "GUÍA DOCENTE {año}" se rinde con una constante. Issue [#222](https://github.com/mmasias/pyCelda/issues/222) para leerlo de la guía cuando `CursoAcademico` exista.
- **`app/render/guia_docente.py` es un módulo de presentación/render, no una capa Service** -- ver la misma decisión en [`descargarGuiaPDF()` en Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md). No introduce Services en pyCelda (Fat Model, discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Profesorado: la copia congelada, sin cambio con #254** -- `_contexto()` sigue leyendo `guia.profesorado` (issue [#254](https://github.com/mmasias/pyCelda/issues/254) no toca el render). Para una `Guia` nunca aprobada la copia está vacía y la fila `DOCENTE` sale "No aplica": aceptable, la banda de aviso ya marca que es un borrador. La previsualización enseña "cómo quedará el documento oficial", no el estado en vivo de la plantilla.

## Referencias

- [`previsualizarGuia()` en Análisis](/RUP/02-analisis/casos-uso/previsualizarGuia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/README.md).
- [`descargarGuiaPDF()` en Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md) -- comparte `app/render/guia_docente.py`; salida PDF, con `alt` sobre `tiene_pdf_generado()`.
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- `_tiene_acceso_a_guia` (rama `Profesor`/`DirectorPrograma`); `previsualizarGuia()` añade la rama `Admin`, como `descargarGuiaPDF()`.
- [`descargarGuiaPDF()` en Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md) -- mismo gate (`admin_email is not None or _tiene_acceso_a_guia(...)`), issue [#262](https://github.com/mmasias/pyCelda/issues/262).
- [Discussion #218](https://github.com/mmasias/pyCelda/discussions/218) -- D1/D4 (plantilla única, dos salidas), P3/P4 (autorización, estados).
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial; la vista HTML conserva la banda roja (no paginada).
