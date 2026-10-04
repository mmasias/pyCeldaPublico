<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarResultadoAprendizajeAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md): **sin `<<choice>>` bloqueante** -- último escalón de la cascada `ResultadoAprendizaje`. La consulta previa (`quedaSinResultadosAprendizajeTrasDesasociar()`) alimenta una advertencia condicional (quedaría sin ningún RA), no un permiso; patrón gemelo de `desasociarMetodologiaDocenteAsignaturaPrograma()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarResultadoAprendizajeAsignaturaProgramaView` (React) -- añade la advertencia condicional al diálogo cuando la respuesta es `true`.
- **API**: `routers/asignatura_programa.py::quedaria_sin_resultados_tras_desasociar(asignatura_programa_id, resultado_aprendizaje_id)` / `::desasociar_resultado_aprendizaje(asignatura_programa_id, resultado_aprendizaje_id)` -- funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- conteo de filas sobre la tabla intermedia, asignado al Repository ya en Análisis.
- **Repositorio**: `AsignaturaProgramaRepository.quedaria_sin_resultados_tras_desasociar(asignatura_programa_id, resultado_aprendizaje_id)` / `.desasociar_resultado_aprendizaje(asignatura_programa_id, resultado_aprendizaje_id)` -- borra de `asignaturas_programa_resultados_aprendizaje`, no del catálogo del `Programa`.

## Decisiones de diseño

- **Consulta de advertencia en el Repository** (`SELECT EXISTS` de "queda algún otro RA"), misma justificación que su gemelo de `MetodologiaDocente`: sin invariante que proteger, no hay método de Modelo.
- **`alt` de dos ramas (confirma/cancela)**: la advertencia no bifurca el flujo de guardado.
- **204 No Content** y cancelación sin llamada HTTP, criterio común del lote.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: endpoint espejo bajo `/api/v1/admin/...` (`GET .../resultados-aprendizaje/{raId}/quedaria-sin-resultados` y `DELETE .../resultados-aprendizaje/{raId}` bajo `/api/v1/admin/asignaturas-programa/{id}`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; reutiliza sin cambios los mismos métodos de repositorio. La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`desasociarResultadoAprendizajeAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- diagrama de colaboración origen; discussion [#33](https://github.com/mmasias/pyCelda/discussions/33).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md).
- [`desasociarResultadoAprendizajeAMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) -- contraste: bloqueante, con rama roja.
- [`asociarResultadoAprendizajeAAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) -- caso de uso complementario.
