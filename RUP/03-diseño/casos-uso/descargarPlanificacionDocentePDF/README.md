<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > descargarPlanificacionDocentePDF() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/README.md)|[Análisis](/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-20
- **Autor**: Claude Opus 5.5 (vía Claude Code)

## Propósito

Bajada a diseño de [`descargarPlanificacionDocentePDF()`](/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/README.md): un endpoint de solo lectura que renderiza en cada petición un PDF propio con la planificación docente de la `Guia`, con el mismo motor y la misma autorización que [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/descargarPlanificacionDocentePDF/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: componente `BotonDescargarPlanificacion` en `AbrirGuia` (sección de planificación docente, junto al número de sesiones), en `PlanificacionDocente` (junto al número de sesiones) y en `ListaGuiasDelPrograma` en modo `admin` (botón de fila). Pide el PDF con `descargarPlanificacionDocentePDF(guiaId)` y lo descarga con el nombre que propone el servidor.
- **API**: `routers/guia.py::descargar_planificacion_docente_pdf(guia_id)` -- función suelta, sin capa Service. Autorización: `admin_email` o `_tiene_acceso_a_guia()` (Profesor que imparte, Director del programa), `404` uniforme.
- **Render**: `render/guia_docente.py::render_planificacion_docente_pdf(guia, db)` y `_contexto_planificacion()`, con la plantilla `templates/planificacion_docente.html`.
- **Repositorio**: `GuiaRepository.obtener(guia_id)`.

## Decisiones de diseño

- **Sin almacenar nada**: se renderiza en cada descarga, como `descargarGuiaPDF()`; no hay `fecha_generacion` ni bloqueo por estado.
- **Marca de agua por estado**: `no_oficial` salvo `EnRevision` y `Aprobada`. En esos dos estados la planificación es la enviada y su uso es responsabilidad del profesor.
- **Solo `Sesion` vinculadas**, ordenadas por `numero` y numeradas de 1 en adelante: lo guardado, no lo que está en la lista de trabajo del navegador.
- **Color por tipo, sin columna de tipo**: la clase de fila (`sesion-teorica`, `sesion-practica`, `sesion-teorico-practica`) y la leyenda son las de la pantalla (`frontend/src/sesionTipo.ts`, colores de `index.css`), repetidas en `_CLASE_SESION`/`_LEYENDA_SESIONES` y en la plantilla. Evaluación continua y parcial, sin color.
- **Una página**: márgenes, letra y relleno de celdas más ajustados que el documento oficial, datos de la asignatura en dos columnas y leyenda bajo la tabla, junto al total: hasta unas 35 sesiones caben en una página.
- **Cabecera y datos de la asignatura** como el documento oficial: logo, curso académico, asignatura, titulación, curso, semestre y docentes (`Guia.profesorado`, la misma copia que usa el documento oficial).
- **Nombre del fichero** en `Content-Disposition`: `Planificacion_<sigla>_<asignatura>_<curso>.pdf`, en ASCII y sin espacios.
- **Estado de la guía en la planificación**: `AbrirPlanificacionDocenteResponse` gana `estado_guia`, para que la pantalla de planificación decida si muestra el mínimo.

## Referencias

- [`descargarPlanificacionDocentePDF()` en Análisis](/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/README.md)
- [`descargarGuiaPDF()` en Diseño](../descargarGuiaPDF/README.md)
