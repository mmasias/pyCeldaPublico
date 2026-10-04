<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSemestreGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarSemestreGuia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarSemestreGuia()`](/RUP/02-analisis/casos-uso/editarSemestreGuia/README.md): `PUT /api/v1/guias/{guia_id}/semestre`, sin `HistorialCambio` (la especificación no lo pide) y con un efecto colateral condicional -- si la `Guia` estaba `Aprobada`, `Guia.regenerar_pdf()` actualiza `fecha_generacion_pdf` sin cambiar `estado`. La generación real del archivo PDF queda deliberadamente fuera de alcance: pertenece a `generarGuiasPDF()`, caso de uso de `Admin` no construido en esta rebanada.

**Ya no es el único disparador de `regenerar_pdf()`** (retoque posterior, discussion [#224](https://github.com/mmasias/pyCelda/discussions/224)): `Guia.aprobar()`/`Guia.escalar_a_aprobada()` llaman al mismo método, como self-call dentro de su propio cuerpo -- ver [Diseño de `aprobarGuia()`](/RUP/03-diseño/casos-uso/aprobarGuia/README.md). Este caso de uso no cambia: sigue siendo el único que lo llama explícitamente desde el Router (los otros dos lo encapsulan en el Modelo), y su condición (`estado == Aprobada`) es la misma.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarSemestreGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarSemestreGuiaView` (React) -- recoge el `semestre`; pide `PUT /api/v1/guias/{guia_id}/semestre`.
- **API**: `routers/guia.py::editar_semestre_guia(guia_id, datos)` -- función nueva.
- **Modelo**: `Guia.actualizar_semestre(semestre)` -- método nuevo; `Guia.regenerar_pdf()` -- método nuevo, condicional a `estado == Aprobada`, sin transición de estado.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`.

## Decisiones de diseño

- **`Guia.regenerar_pdf()` no genera ningún archivo real en esta rebanada**: solo actualiza `fecha_generacion_pdf` -- el mecanismo real de generación (motor de PDF, almacenamiento) pertenece a `generarGuiasPDF()`, fuera de alcance de este lote de 12. Documentado explícitamente en el diagrama de secuencia para no confundirlo con un hueco.
- **Sin `HistorialCambio`**: a diferencia de `rechazarGuia()`/`escalarGuiaAAprobada()`/`revocarAprobacionGuia()`, la especificación de Requisitos no pide registrar este cambio -- no se añade por simetría con las demás.
- **Sin `alt`**: el efecto colateral es condicional en prosa (nota en el diagrama), no una rama de la secuencia -- mismo mecanismo que `guardarBorradorGuia()` usa para "si estaba Aprobada, pasa a Borrador".
- **Sin capa Service**: Router delgado -> Modelo/Repository.

## Referencias

- [`editarSemestreGuia()` en Análisis](/RUP/02-analisis/casos-uso/editarSemestreGuia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/README.md).
- [`guardarBorradorGuia()` en Diseño](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- mismo mecanismo narrativo para un efecto colateral condicional.
- [`descargarGuiaPDF()` en Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md) -- consumidor de `fecha_generacion_pdf`, actualizado aquí cuando aplica (y, desde discussion #224, también por `aprobarGuia()`/`escalarGuiaAAprobada()`).
- [`aprobarGuia()` en Diseño](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- disparador nuevo del mismo `regenerar_pdf()`, como self-call en vez de paso explícito del Router.
