<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarMetodologiaDocenteAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md): **sin `<<choice>>` bloqueante** -- `AsignaturaPrograma` es el último escalón de la cascada, no hay nivel inferior que proteger. La consulta previa (`quedaSinMetodologiasDocentesTrasDesasociar()`) no decide permiso sino advertencia: si la `MetodologiaDocente` es la única, el diálogo avisa de que la asignatura quedaría sin ninguna, pero el `DELETE` se ejecuta igual.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarMetodologiaDocenteAsignaturaProgramaView` (React) -- añade la advertencia condicional al diálogo de confirmación cuando la respuesta es `true`.
- **API**: `routers/asignatura_programa.py::quedaria_sin_metodologias_tras_desasociar(asignatura_programa_id, metodologia_docente_id)` / `::desasociar_metodologia_docente(asignatura_programa_id, metodologia_docente_id)` -- funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- la pregunta es un conteo sobre la tabla intermedia, Análisis ya la asignaba al Repository.
- **Repositorio**: `AsignaturaProgramaRepository.quedaria_sin_metodologias_tras_desasociar(asignatura_programa_id, metodologia_docente_id)` (un `SELECT EXISTS` de "queda alguna otra") / `.desasociar_metodologia_docente(asignatura_programa_id, metodologia_docente_id)`.

## Decisiones de diseño

- **Consulta de advertencia en el Repository, no en el Modelo**: a diferencia de los dos `desasociar*DeMateria()` (cuya regla de bloqueo es una invariante y vive en `Materia`), aquí la pregunta es un conteo de filas sin lectura de negocio -- Análisis la asignaba ya al `AsignaturaProgramaRepository`, Diseño la traduce como `SELECT EXISTS` directo.
- **El `alt` tiene solo dos ramas (confirma/cancela)**: la advertencia condicional no bifurca el flujo -- con o sin advertencia, la confirmación ejecuta el mismo `DELETE`. Es la diferencia estructural con los bloqueantes de este mismo lote, que tienen rama roja propia.
- **204 No Content** y rama de cancelación sin llamada HTTP, mismo criterio del lote.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: endpoint espejo bajo `/api/v1/admin/...` (`GET .../metodologias-docentes/{mdId}/quedaria-sin-metodologias` y `DELETE .../metodologias-docentes/{mdId}` bajo `/api/v1/admin/asignaturas-programa/{id}`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; reutiliza sin cambios los mismos métodos de repositorio. La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`desasociarMetodologiaDocenteAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md) -- diagrama de colaboración origen; discussion [#33](https://github.com/mmasias/pyCelda/discussions/33) (cierre sin bloqueo).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md).
- [`desasociarMetodologiaDocenteMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- contraste: bloqueante, con rama roja.
- [`desasociarResultadoAprendizajeAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- patrón gemelo con el otro asociado.
