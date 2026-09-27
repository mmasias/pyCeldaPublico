<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarResultadoAprendizajeAsignaturaGrado()`](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md): **sin `<<choice>>` bloqueante** -- último escalón de la cascada `ResultadoAprendizaje`. La consulta previa (`quedaSinResultadosAprendizajeTrasDesasociar()`) alimenta una advertencia condicional (quedaría sin ningún RA), no un permiso; patrón gemelo de `desasociarMetodologiaDocenteAsignaturaGrado()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarResultadoAprendizajeAsignaturaGradoView` (React) -- añade la advertencia condicional al diálogo cuando la respuesta es `true`.
- **API**: `routers/asignatura_grado.py::quedaria_sin_resultados_tras_desasociar(asignatura_grado_id, resultado_aprendizaje_id)` / `::desasociar_resultado_aprendizaje(asignatura_grado_id, resultado_aprendizaje_id)` -- funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- conteo de filas sobre la tabla intermedia, asignado al Repository ya en Análisis.
- **Repositorio**: `AsignaturaGradoRepository.quedaria_sin_resultados_tras_desasociar(asignatura_grado_id, resultado_aprendizaje_id)` / `.desasociar_resultado_aprendizaje(asignatura_grado_id, resultado_aprendizaje_id)` -- borra de `asignaturas_grado_resultados_aprendizaje`, no del catálogo del `Grado`.

## Decisiones de diseño

- **Consulta de advertencia en el Repository** (`SELECT EXISTS` de "queda algún otro RA"), misma justificación que su gemelo de `MetodologiaDocente`: sin invariante que proteger, no hay método de Modelo.
- **`alt` de dos ramas (confirma/cancela)**: la advertencia no bifurca el flujo de guardado.
- **204 No Content** y cancelación sin llamada HTTP, criterio común del lote.

## Referencias

- [`desasociarResultadoAprendizajeAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- diagrama de colaboración origen; discussion [#33](https://github.com/mmasias/pyCelda/discussions/33).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md).
- [`desasociarResultadoAprendizajeAMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) -- contraste: bloqueante, con rama roja.
- [`asociarResultadoAprendizajeAAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md) -- caso de uso complementario.
