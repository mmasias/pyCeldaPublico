<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarMetodologiaDocenteAAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md): sin `<<choice>>` -- segundo escalón de la cascada `MetodologiaDocente`. Agregación simple (`AsignaturaPrograma o-r- MetodologiaDocente`, sin clase de asociación), con una regla de consistencia en el listado de disponibles: solo `MetodologiaDocente` ya asociadas a la `Materia` y aún no asociadas a esta `AsignaturaPrograma`. `AsignaturaProgramaController` converge en `routers/asignatura_programa.py`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarMetodologiaDocenteAAsignaturaProgramaView` (React) -- selector del subconjunto válido; pide `GET .../disponibles` y `POST /api/v1/asignaturas-programa/{asignatura_programa_id}/metodologias-docentes`.
- **API**: `routers/asignatura_programa.py::listar_metodologias_docentes_disponibles(asignatura_programa_id)` / `::asociar_metodologia_docente(asignatura_programa_id, datos)` -- funciones sueltas del módulo nuevo.
- **Modelo**: `AsignaturaPrograma` gana una `MetodologiaDocente` en su colección -- sin método invocado; `MetodologiaDocente` porta `codigo`/`descripcion`.
- **Repositorio**: `MetodologiaDocenteRepository.listar_disponibles_para_asignatura_programa(asignatura_programa_id)` -- aplica la regla de consistencia en la consulta; `AsignaturaProgramaRepository.asociar_metodologia_docente(asignatura_programa_id, metodologia_docente_id)` -- `INSERT` en la tabla intermedia.

## Decisiones de diseño

- **La regla de consistencia (subconjunto de la `Materia`) vive en la consulta de disponibles**, donde Análisis la puso (`MetodologiaDocenteRepository.listarDisponiblesParaAsignaturaPrograma()`): un solo `SELECT` con tres joins resuelve "asociadas a la `Materia` Y no asociadas aún a esta `AsignaturaPrograma`". El `POST` no revalida: el selector solo ofrece opciones válidas y no hay invariante de estado que proteger (la desasociación del nivel inferior es libre).
- **`AsignaturaProgramaRepository` persiste su tabla intermedia** (`asignaturas_programa_metodologias_docentes`), igual que `MateriaRepository` persistía la suya en el par de `ResultadoAprendizaje` -- sin clase de asociación no hay repositorio propio de la tabla.
- **204 No Content**: agregación simple, sin entidad nueva que devolver.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: endpoint espejo bajo `/api/v1/admin/...` (`GET`/`POST /api/v1/admin/asignaturas-programa/{id}/metodologias-docentes[/disponibles]`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; reutiliza sin cambios los mismos métodos de repositorio. La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`asociarMetodologiaDocenteAAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md).
- [`asociarMetodologiaDocenteAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la cascada; contraste en el filtro de disponibles (catálogo institucional completo).
- [`desasociarMetodologiaDocenteAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md) -- caso de uso complementario.
