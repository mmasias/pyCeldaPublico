<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarMetodologiaDocenteAMateria()`](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/README.md): patrón C→U, sin `<<choice>>` -- dos interacciones (cargar disponibles, asociar) contra `MateriaController` (B/C/E), que converge en `routers/materia.py`. Crea real e inmediato la fila `MetodologiaMateria` con `descripcion_propia` vacía.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarMetodologiaDocenteAMateriaView` (React) -- selector de `MetodologiaDocente` del catálogo institucional aún no asociadas; pide `GET .../disponibles` y `POST /api/v1/materias/{materia_id}/metodologias-docentes`.
- **API**: `routers/materia.py::listar_metodologias_docentes_disponibles(materia_id)` / `::asociar_metodologia_docente(materia_id, datos)` -- funciones sueltas del módulo nuevo de `Materia`.
- **Modelo**: `MetodologiaMateria` nace con `descripcion_propia` vacía -- sin método invocado; `MetodologiaDocente` solo porta `codigo`/`descripcion` para el selector.
- **Repositorio**: `MetodologiaDocenteRepository.listar_disponibles_para_materia(materia_id)` -- el filtro "no asociadas aún" vive en la consulta; `MetodologiaMateriaRepository.crear(materia_id, metodologia_docente_id)` -- `INSERT` inmediato.

## Decisiones de diseño

- **El filtro de disponibles vive en el Repository, no en el Modelo**: Análisis asigna `listarDisponiblesParaMateria(materiaId)` a `MetodologiaDocenteRepository` -- un `LEFT JOIN ... WHERE mm.id IS NULL` resuelve "catálogo institucional menos las ya asociadas" en una consulta; no hay regla de negocio que justifique un método de Modelo.
- **Dos Repository, uno por tabla**: el listado consulta `metodologias_docentes` (dominio de `MetodologiaDocenteRepository`), la asociación inserta en `metodologias_materia` (dominio de `MetodologiaMateriaRepository`) -- cada repositorio persiste una sola tabla, sin cruzar responsabilidades.
- **`MetodologiaMateriaCreate` solo transporta `metodologia_docente_id`**: `materia_id` va en la URL y `descripcion_propia` nace vacía por defecto -- quien la completa después es `editarAsociacionMetodologiaDocenteMateria()`.
- **201 Created**: devuelve la asociación creada con su contenido (útil para que la Vista la pinte sin recargar).

## Referencias

- [`asociarMetodologiaDocenteAMateria()` en Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md).
- [`asociarMetodologiaDocenteAAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md) -- segundo escalón de la cascada; contrasta en el filtro de disponibles (subconjunto de la `Materia`, no catálogo completo).
