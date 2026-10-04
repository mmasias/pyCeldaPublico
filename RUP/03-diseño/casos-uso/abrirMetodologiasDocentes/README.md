<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentes() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirMetodologiasDocentes()`](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md): un solo paso, de solo lectura. Presenta el listado completo de `MetodologiaDocente` -- catálogo institucional plano que cuelga directamente de `SISTEMA_DISPONIBLE` (entrada directa desde `abrirPanelAdministracion()`, sin composición padre). Cada fila presenta `codigo` y `descripcion`. `MetodologiaDocenteController` converge en `routers/metodologia_docente.py`, módulo nuevo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirMetodologiasDocentesView` (React) -- ofrece un selector de `Universidad` y pide `GET /api/v1/universidades/{universidad_id}/metodologias-docentes` de la elegida; presenta `codigo` y `descripcion` por fila.
- **API**: `routers/metodologia_docente.py::listar_metodologias_docentes(universidad_id)` -- función suelta, primera del módulo nuevo.
- **Modelo**: ninguno con lógica propia invocada -- `MetodologiaDocente` solo porta los datos de cada fila.
- **Repositorio**: `MetodologiaDocenteRepository.listar_de_la_universidad(universidad_id)` -- `SELECT` filtrado por `universidad_id`: el listado es el catálogo de `MetodologiaDocente` de la `Universidad` elegida, no una selección propia de quien llama. El repositorio ya existía con las queries de disponibilidad para asociación; gana aquí su primer método de catálogo propio.

## Decisiones de diseño

- **Módulo `routers/metodologia_docente.py` nuevo**: primera función de `MetodologiaDocente` fuera de las asociaciones (que viven en `routers/materia.py`/`routers/asignatura_programa.py`); el módulo crecerá con `obtener_metodologia_docente()` (de `abrirMetodologiaDocente()`), `crear_metodologia_docente()`, `editar_metodologia_docente()` y `eliminar_metodologia_docente()` de los CU hermanos.
- **Listado completo, sin filtro por sesión**: igual que `abrirAsignaturas()`, aquí el `Admin` ve todas las filas -- ninguna `MetodologiaDocente` es "propia" de quien llama. A diferencia de las variantes `DirectorPrograma` (`listar_disponibles_para_materia()`/`listar_disponibles_para_asignatura_programa()`), este endpoint no filtra por disponibilidad de asociación.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py`, sin nota de pendiente: toda función de `routers/metodologia_docente.py` la declara explícitamente. Es catálogo de `Admin` sin pertenencia que verificar -- no usa `get_current_director_programa_id`, que aplica a los recursos con dueño del hilo `DirectorPrograma`. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirMetodologiasDocentes()` en Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md).
- [`abrirMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) / [`crearMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md) / [`eliminarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) -- destinos de navegación del listado.
- [`abrirAsignaturas()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md) -- mismo patrón de listado plano sin filtro por sesión.
