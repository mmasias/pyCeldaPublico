<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturas/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirAsignaturas()`](/RUP/02-analisis/casos-uso/abrirAsignaturas/README.md): un solo paso, de solo lectura. Presenta el listado completo de `Asignatura` -- catálogo institucional plano que cuelga directamente de `SISTEMA_DISPONIBLE` (sin composición padre, a diferencia de `Facultad` bajo `Universidad`). Cada fila presenta `nombre`, `ects` y `estado`. `AsignaturaController` converge en `routers/asignatura.py`, módulo nuevo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirAsignaturas/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirAsignaturasView` (React) -- pide `GET /api/v1/asignaturas`; presenta `nombre`, `ects` y `estado` por fila.
- **API**: `routers/asignatura.py::listar_asignaturas()` -- función suelta, primera del módulo nuevo.
- **Modelo**: ninguno con lógica propia invocada -- `Asignatura` solo porta los datos de cada fila.
- **Repositorio**: `AsignaturaRepository.listar()` -- `SELECT` sin filtro: el listado es la totalidad del catálogo de `Asignatura`, no una selección propia de quien llama.

## Decisiones de diseño

- **Módulo `routers/asignatura.py` nuevo**: primera función de `Asignatura` en Diseño; el módulo crecerá con `obtener_asignatura()` (de `abrirAsignatura()`), `crear_asignatura()`, `editar_asignatura()` y `eliminar_asignatura()` de los CU hermanos.
- **Listado completo, sin filtro por sesión**: a diferencia de `abrirProgramas()` (variante `DirectorPrograma`, filtrado por cookie JWT de la discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)), aquí el `Admin` ve todas las filas -- ninguna `Asignatura` es "propia" de quien llama, igual que en `abrirUniversidades()`.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente: toda función de `routers/asignatura.py` la declara explícitamente. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor -- se deja constancia explícita en cada CU de este lote, no solo en uno.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirAsignaturas()` en Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturas/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/README.md).
- [`abrirAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md) / [`crearAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignatura/README.md) / [`eliminarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md) -- destinos de navegación del listado.
- [`abrirUniversidades()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidades/README.md) -- mismo patrón de listado plano sin filtro por sesión.
