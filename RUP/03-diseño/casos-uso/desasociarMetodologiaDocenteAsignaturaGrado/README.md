<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarMetodologiaDocenteAsignaturaGrado()`](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md): **sin `<<choice>>` bloqueante** -- `AsignaturaGrado` es el último escalón de la cascada, no hay nivel inferior que proteger. La consulta previa (`quedaSinMetodologiasDocentesTrasDesasociar()`) no decide permiso sino advertencia: si la `MetodologiaDocente` es la única, el diálogo avisa de que la asignatura quedaría sin ninguna, pero el `DELETE` se ejecuta igual.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarMetodologiaDocenteAsignaturaGradoView` (React) -- añade la advertencia condicional al diálogo de confirmación cuando la respuesta es `true`.
- **API**: `routers/asignatura_grado.py::quedaria_sin_metodologias_tras_desasociar(asignatura_grado_id, metodologia_docente_id)` / `::desasociar_metodologia_docente(asignatura_grado_id, metodologia_docente_id)` -- funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- la pregunta es un conteo sobre la tabla intermedia, Análisis ya la asignaba al Repository.
- **Repositorio**: `AsignaturaGradoRepository.quedaria_sin_metodologias_tras_desasociar(asignatura_grado_id, metodologia_docente_id)` (un `SELECT EXISTS` de "queda alguna otra") / `.desasociar_metodologia_docente(asignatura_grado_id, metodologia_docente_id)`.

## Decisiones de diseño

- **Consulta de advertencia en el Repository, no en el Modelo**: a diferencia de los dos `desasociar*DeMateria()` (cuya regla de bloqueo es una invariante y vive en `Materia`), aquí la pregunta es un conteo de filas sin lectura de negocio -- Análisis la asignaba ya al `AsignaturaGradoRepository`, Diseño la traduce como `SELECT EXISTS` directo.
- **El `alt` tiene solo dos ramas (confirma/cancela)**: la advertencia condicional no bifurca el flujo -- con o sin advertencia, la confirmación ejecuta el mismo `DELETE`. Es la diferencia estructural con los bloqueantes de este mismo lote, que tienen rama roja propia.
- **204 No Content** y rama de cancelación sin llamada HTTP, mismo criterio del lote.

## Referencias

- [`desasociarMetodologiaDocenteAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md) -- diagrama de colaboración origen; discussion [#33](https://github.com/mmasias/pyCelda/discussions/33) (cierre sin bloqueo).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md).
- [`desasociarMetodologiaDocenteMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- contraste: bloqueante, con rama roja.
- [`desasociarResultadoAprendizajeAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- patrón gemelo con el otro asociado.
