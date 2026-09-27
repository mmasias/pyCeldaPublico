<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarMetodologiaDocenteAAsignaturaGrado()`](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md): sin `<<choice>>` -- segundo escalón de la cascada `MetodologiaDocente`. Agregación simple (`AsignaturaGrado o-r- MetodologiaDocente`, sin clase de asociación), con una regla de consistencia en el listado de disponibles: solo `MetodologiaDocente` ya asociadas a la `Materia` y aún no asociadas a esta `AsignaturaGrado`. `AsignaturaGradoController` converge en `routers/asignatura_grado.py`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarMetodologiaDocenteAAsignaturaGradoView` (React) -- selector del subconjunto válido; pide `GET .../disponibles` y `POST /api/v1/asignaturas-grado/{asignatura_grado_id}/metodologias-docentes`.
- **API**: `routers/asignatura_grado.py::listar_metodologias_docentes_disponibles(asignatura_grado_id)` / `::asociar_metodologia_docente(asignatura_grado_id, datos)` -- funciones sueltas del módulo nuevo.
- **Modelo**: `AsignaturaGrado` gana una `MetodologiaDocente` en su colección -- sin método invocado; `MetodologiaDocente` porta `codigo`/`descripcion`.
- **Repositorio**: `MetodologiaDocenteRepository.listar_disponibles_para_asignatura_grado(asignatura_grado_id)` -- aplica la regla de consistencia en la consulta; `AsignaturaGradoRepository.asociar_metodologia_docente(asignatura_grado_id, metodologia_docente_id)` -- `INSERT` en la tabla intermedia.

## Decisiones de diseño

- **La regla de consistencia (subconjunto de la `Materia`) vive en la consulta de disponibles**, donde Análisis la puso (`MetodologiaDocenteRepository.listarDisponiblesParaAsignaturaGrado()`): un solo `SELECT` con tres joins resuelve "asociadas a la `Materia` Y no asociadas aún a esta `AsignaturaGrado`". El `POST` no revalida: el selector solo ofrece opciones válidas y no hay invariante de estado que proteger (la desasociación del nivel inferior es libre).
- **`AsignaturaGradoRepository` persiste su tabla intermedia** (`asignaturas_grado_metodologias_docentes`), igual que `MateriaRepository` persistía la suya en el par de `ResultadoAprendizaje` -- sin clase de asociación no hay repositorio propio de la tabla.
- **204 No Content**: agregación simple, sin entidad nueva que devolver.

## Referencias

- [`asociarMetodologiaDocenteAAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md).
- [`asociarMetodologiaDocenteAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la cascada; contraste en el filtro de disponibles (catálogo institucional completo).
- [`desasociarMetodologiaDocenteAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md) -- caso de uso complementario.
