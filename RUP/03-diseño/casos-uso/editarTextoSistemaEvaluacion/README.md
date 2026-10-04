<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarTextoSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarTextoSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md) (issue [#610](https://github.com/mmasias/pyCelda/issues/610)): el Profesor edita `Guia.texto_sistema_evaluacion`, el texto de convocatorias del apartado 5 de la guía. Mismo patrón de edición simple que [`editarSistemaEvaluacion()`](../editarSistemaEvaluacion/README.md) (cargar por Repository, mutar, persistir), con una diferencia: aquí **sí hay rama de fallo**, la guardia de forma `[TABLA]` exactamente una vez (`422`), y la entidad editada es la `Guia` del Profesor, no un catálogo de Admin.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarTextoSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `PonderacionesEvaluacion` (React, ruta `/guias/:guiaId/ponderaciones-evaluacion`) -- `<textarea>` precargado con `guia.texto_sistema_evaluacion` (del `GET` de la guía que ya hace la pantalla) y tres plantillas de frontend (`textoSistemaEvaluacion.ts`: asignatura normal, prácticas externas, prácticas de laboratorio) que rellenan sin guardar. Cuenta los marcadores en cliente y deshabilita "Guardar texto" si no hay exactamente uno. Pide `PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion` con `{ texto }`.
- **API**: `routers/guia.py::editar_texto_sistema_evaluacion(guia_id, datos)` -- función suelta, sin capa Service. Autorización `get_current_profesor_id` + `AsignaturaProgramaRepository.imparte(...)`.
- **Modelo**: `Guia.texto_sistema_evaluacion` (columna `Text`, `default=""`) y constante `MARCADOR_TABLA = "[TABLA]"`. No hay método de dominio: el Router asigna el atributo directamente.
- **Repositorios**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`; `AsignaturaProgramaRepository.imparte(asignatura_programa_id, profesor_id)`.

## Decisiones de diseño

- **Endpoint propio, independiente de `guardarBorradorGuia()`**: el texto se guarda por su cuenta, sin pasar por el borrador de la guía.
- **Guardia de forma en Router**: `texto.count(MARCADOR_TABLA) != 1` -> `422` con detalle `El texto debe contener el marcador [TABLA] exactamente una vez`. Se comprueba en **cada** guardado; nada se persiste si falla.
- **`404` uniforme** si la guía no existe, no tiene `asignatura_programa_id` o el Profesor no imparte la asignatura. Admin y Director quedan fuera hasta [#601](https://github.com/mmasias/pyCelda/issues/601).
- **Sin efectos colaterales de guía**: el handler no registra `HistorialCambio`, no llama a `confirmar_guardado()` ni a `regenerar_pdf()`. Persiste con `GuiaRepository.actualizar(guia)` (commit + refresh) y devuelve `GuiaResponse`.
- **Patrón B (clonado entre cursos)**: `texto_sistema_evaluacion` se copia de la `Guia` previa en [`activarCursoAcademico()`](../activarCursoAcademico/README.md); sin predecesora nace vacío. No es parte de este flujo.
- **Render tolerante**: `render/guia_docente.py` parte el texto por `[TABLA]` (antes / tabla de ponderaciones / después); un dato legado sin exactamente un marcador se pinta entero como "antes" sin fallar. Tras la sección va siempre el párrafo fijo de régimen de uso de IA.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`editarTextoSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/README.md).
- [`editarSistemaEvaluacion()` en Diseño](../editarSistemaEvaluacion/README.md) -- plantilla de edición simple.
- [`activarCursoAcademico()` en Diseño](../activarCursoAcademico/README.md) -- clonado del texto entre cursos.
