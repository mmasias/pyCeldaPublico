<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDeGuiaHermana() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md)|[Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-05
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño de [`importarPlanificacionDocenteDeGuiaHermana()`](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)). Gemelo de [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) sobre `Sesion` en vez de `ReferenciaBibliografica`. **Toda la ficha de Diseño del gemelo aplica** -- endpoints en el mismo router `importar_guia_hermana.py`, mismo `GET /importables` compartido, misma autorización, mismo patrón de un-solo-commit y borrado vía ORM. A continuación solo lo específico.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDeGuiaHermana/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Específico de la planificación docente

- **Endpoint**: `POST /api/v1/guias/{guia_id}/importar-planificacion-docente`, body `{origen_guia_id: int}`, respuesta `GuiaResponse`.
- **`SesionRepository.reemplazar_desde(guia_destino, sesiones_origen)`**: borra vía ORM todas las `Sesion` del destino y crea copias `sorted(sesiones_origen, key=numero)` con `numero = 1..N` **en persistencia** -- a diferencia de [`eliminarSesion()`](/RUP/03-diseño/casos-uso/eliminarSesion/README.md), donde la renumeración es solo posicional; aquí las filas son nuevas y `1..N` es su valor de alta. Replica `tipo`, `descripcion` y `vinculada` fila a fila. **No toca `Guia.sesiones_minimas`** del destino (config de su propia `AsignaturaPrograma`, umbral de la regla `c3` de `enviarGuiaARevision()`, discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)).
- **`HistorialCambio`**: `campo="planificacion_docente"`, `comentario="planificación docente importada desde {programa} / {codigo}"`.
- **Vista**: `ImportarPlanificacionDocenteDeGuiaHermana.tsx` (ruta `/guias/:guiaId/importar-planificacion-docente`); botón en `PlanificacionDocente.tsx`; al confirmar, `limpiarExcluidos(claveSesionesExcluidas(guiaId))`.
- **Divergencia lateral registrada** (no la resuelve este CU): el Modelo declara `Guia *-- PlanificacionDocente *-- Sesion`; el código aplana `Sesion.guia_id` directo. `reemplazar_desde` opera sobre `Sesion.guia_id` como el resto del código -- no añade lógica que dependa de una `PlanificacionDocente` intermedia.

## Referencias

- [`importarBibliografiaDeGuiaHermana()` en Diseño](../importarBibliografiaDeGuiaHermana/README.md) -- ficha completa de la mecánica compartida.
- [`importarPlanificacionDocenteDeGuiaHermana()` en Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md).
- [`enviarGuiaARevision()` en Detalle](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md) -- regla `c3` (`sesiones_minimas`) que este CU no altera.
