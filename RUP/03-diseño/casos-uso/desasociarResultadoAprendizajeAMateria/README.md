<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarResultadoAprendizajeAMateria()`](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/README.md): `<<choice>>` bloqueante -- rompe la asociación `Materia`-`ResultadoAprendizaje` solo si ninguna `AsignaturaPrograma` de esa `Materia` tiene ya asignado el mismo `ResultadoAprendizaje` (integridad de la cascada: los RA de una `AsignaturaPrograma` son subconjunto de los de su `Materia`). Estructura espejo de `desasociarMetodologiaDocenteMateria()`.

**Retocado (issue #179, 2026-09-05)**: mismo retoque que su gemelo -- `tiene_resultado_aprendizaje_en_uso() : bool` pasa a `asignaturas_programa_con_resultado_aprendizaje() : list[str]`, endpoint de chequeo de `bool` a `list[str]`, `DELETE` reverifica y construye el 409 con nombres reales.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarResultadoAprendizajeAMateriaView` (React) -- pide la lista de bloqueo antes de confirmar; en la rama bloqueada presenta el motivo con los nombres reales.
- **API**: `routers/materia.py::puede_desasociar_resultado_aprendizaje(materia_id, resultado_aprendizaje_id)` / `::desasociar_resultado_aprendizaje(materia_id, resultado_aprendizaje_id)` -- funciones sueltas.
- **Modelo**: `Materia.asignaturas_programa_con_resultado_aprendizaje(resultado_aprendizaje_id)` -- Fat Model: recorre sus `AsignaturaPrograma` y devuelve los nombres de las que ya lo tienen asignado.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` (con las asociadas cargadas) / `.desasociar_resultado_aprendizaje(materia_id, resultado_aprendizaje_id)` -- borra la fila de `materias_resultados_aprendizaje`, no el `ResultadoAprendizaje`.

## Decisiones de diseño

- **Regla de bloqueo en el Modelo** (`Materia.asignaturas_programa_con_resultado_aprendizaje()`), como en Análisis -- misma estructura y justificación que `desasociarMetodologiaDocenteMateria()`: una sola fuente de verdad de la invariante, evaluada sobre el objeto con sus relaciones cargadas.
- **`asignaturas_programa_con_resultado_aprendizaje()` reemplaza `tiene_resultado_aprendizaje_en_uso()` (issue #179)**, mismo criterio que su gemelo de `MetodologiaDocente`: la lista es la fuente de verdad única, el booleano se deriva trivialmente donde hiciera falta.
- **El endpoint de chequeo cambia de contrato: `bool` -> `list[str]`** (`[]` = no bloqueado) -- único consumidor verificado antes de cambiarlo.
- **El `DELETE` reverifica antes de borrar**, 409 con el mismo formato de nombres que el precedente de `ResultadoAprendizaje` (`eliminarResultadoAprendizaje()`, PR #178).
- **Dos endpoints (chequeo + `DELETE`)** y **204 No Content**, idéntico criterio al del par de `MetodologiaDocente`.
- **La rama "cancelada" no genera llamada HTTP** -- rama del `alt` solo para reflejar la salida azul de Análisis.

## Referencias

- [`desasociarResultadoAprendizajeAMateria()` en Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/README.md).
- [`desasociarMetodologiaDocenteMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- patrón gemelo con el otro asociado.
- [`desasociarResultadoAprendizajeAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- contraste: último escalón, sin bloqueo.
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- precedente del patrón de mensaje con nombres reales (PR #178), auditado y replicado aquí (issue #179).
