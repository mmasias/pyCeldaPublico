<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarResultadoAprendizajeAMateria()`](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/README.md): sin `<<choice>>` -- asociación simple (sin clase de asociación ni atributo propio, a diferencia del par `MetodologiaMateria`). Ambas operaciones de Análisis (listar disponibles, asociar) caen en `MateriaRepository`: la tabla intermedia `materias_resultados_aprendizaje` es dominio de la `Materia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarResultadoAprendizajeAMateriaView` (React) -- selector de `ResultadoAprendizaje` del catálogo del `Programa` aún no asociados a la `Materia`; pide `GET .../disponibles` y `POST /api/v1/materias/{materia_id}/resultados-aprendizaje`.
- **API**: `routers/materia.py::listar_resultados_aprendizaje_disponibles(materia_id)` / `::asociar_resultado_aprendizaje(materia_id, datos)` -- funciones sueltas.
- **Modelo**: `Materia` gana un `ResultadoAprendizaje` en su colección -- sin método invocado; la agregación es un `INSERT` en la tabla intermedia.
- **Repositorio**: `MateriaRepository.listar_resultados_aprendizaje_disponibles(materia_id)` / `.asociar_resultado_aprendizaje(materia_id, resultado_aprendizaje_id)` -- ambos sobre `materias_resultados_aprendizaje`.

## Decisiones de diseño

- **`MateriaRepository`, no un repositorio de la tabla intermedia**: Análisis ya lo decidía así -- al no haber clase de asociación con vida propia, la tabla `materias_resultados_aprendizaje` se gestiona desde el repositorio del agregado (`Materia`). Contraste deliberado con `MetodologiaMateriaRepository`, que sí existe porque `MetodologiaMateria` tiene atributo propio.
- **El filtro de disponibles restringe al catálogo del `Programa`**: la consulta parte de `resultados_aprendizaje` del `Programa` de la `Materia` (por `Programa *-d- ResultadoAprendizaje`) y excluye los ya asociados -- la regla vive en la consulta, sin método de Modelo.
- **204 No Content**, no 201: no se crea ninguna entidad nueva -- solo una fila en la tabla intermedia; no hay `XxxResponse` que devolver más allá del código de estado.
- **`AsociarResultadoAprendizajeCreate` transporta solo `resultado_aprendizaje_id`** -- `materia_id` va en la URL.

## Referencias

- [`asociarResultadoAprendizajeAMateria()` en Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md).
- [`asociarMetodologiaDocenteAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- contraste: asociación CON clase de asociación.
- [`asociarResultadoAprendizajeAAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) -- segundo escalón de la misma cascada.
