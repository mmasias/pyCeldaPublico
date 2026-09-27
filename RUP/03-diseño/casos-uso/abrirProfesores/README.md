<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirProfesores() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirProfesores/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirProfesores()`](/RUP/02-analisis/casos-uso/abrirProfesores/README.md): un solo paso, de solo lectura. Presenta el listado completo de `Profesor` -- catálogo institucional top-level que cuelga directamente de `SISTEMA_DISPONIBLE` (entrada directa desde `abrirPanelAdministracion()`, sin composición padre, como `MetodologiaDocente`). Cada fila presenta `nombre` y `email`. `ProfesorController` converge en `routers/profesor.py`, módulo nuevo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirProfesores/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirProfesoresView` (React) -- pide `GET /api/v1/profesores`; presenta `nombre` y `email` por fila.
- **API**: `routers/profesor.py::listar_profesores()` -- función suelta, primera del módulo nuevo.
- **Modelo**: ninguno con lógica propia invocada -- `Profesor` solo porta los datos de cada fila.
- **Repositorio**: `ProfesorRepository.listar()` -- `SELECT` sin filtro: el listado es la totalidad del catálogo de `Profesor`, no una selección propia de quien llama. El repositorio ya existía con `obtener_por_email()` (resolución de rol en el login); gana aquí sus primeros métodos de catálogo propio.

## Decisiones de diseño

- **Módulo `routers/profesor.py` nuevo**: primera función de `Profesor` propia del catálogo (el email de `Profesor` ya aparecía en `routers/auth.py` y en `routers/asignatura_grado.py` como `profesorado`, pero sin CRUD propio); el módulo crecerá con los 6 endpoints de los CU hermanos más el selector de disponibilidad.
- **Listado completo, sin filtro por sesión**: igual que `abrirAsignaturas()`/`abrirMetodologiasDocentes()`, aquí el `Admin` ve todas las filas -- ningún `Profesor` es "propio" de quien llama.
- **Autorización de `Admin`: `Depends(require_admin)`** -- toda función de `routers/profesor.py` la declara explícitamente. Es catálogo de `Admin` sin pertenencia que verificar -- no usa `get_current_director_grado_id`, que aplica a los recursos con dueño del hilo `DirectorGrado`. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirProfesores()` en Análisis](/RUP/02-analisis/casos-uso/abrirProfesores/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/README.md).
- [`abrirProfesor()` en Diseño](/RUP/03-diseño/casos-uso/abrirProfesor/README.md) / [`crearProfesor()` en Diseño](/RUP/03-diseño/casos-uso/crearProfesor/README.md) / [`eliminarProfesor()` en Diseño](/RUP/03-diseño/casos-uso/eliminarProfesor/README.md) -- destinos de navegación del listado.
- [`abrirMetodologiasDocentes()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md) -- mismo patrón de listado plano sin filtro por sesión.
