<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > definirDirectorGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/definirDirectorGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`definirDirectorGrado()`](/RUP/02-analisis/casos-uso/definirDirectorGrado/README.md): alta del rol `DirectorGrado` sobre un `Profesor` ya abierto, sin `<<choice>>` (cardinalidad muchos a muchos libre, discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)). Dos endpoints: el selector carga los `Grado` disponibles (`GET .../grados-disponibles-para-dirigir`) y la confirmación ejecuta la asignación (`POST .../directores-grado`). El mecanismo replica el patrón verificado de `app/scripts/definir_director_grado.py` (que queda como herramienta de operación manual, superseded sin conflicto): resolver el `DirectorGrado` por email -- creándolo si no existía -- e añadir el `Grado` si no estaba ya.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/definirDirectorGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DefinirDirectorGradoView` (React) -- un `<select>` con los `Grado` que el `Profesor` todavía no dirige (`codigo -- nombre`); al confirmar, `POST`; vuelve al detalle.
- **API**: `routers/profesor.py::listar_grados_disponibles_para_dirigir(profesor_id)` / `.definir_director_grado(profesor_id, datos)` -- `404` si el `Profesor` o el `Grado` no existen.
- **Modelo**: la asociación vive en la tabla M2M `grados_directores_grado` (`Grado.directores`) -- sin método de dominio propio; el router muta la colección.
- **Repositorio**: `DirectorGradoRepository.obtener_por_email()` / `.crear(email)` (resolución del rol con creación bajo demanda), `GradoRepository.listar_disponibles_para_dirigir(director_grado_id | None)` (nuevo) / `.obtener()`, `ProfesorRepository.obtener()`.

## Decisiones de diseño

- **Idempotente, mismo criterio que el script CLI**: reejecutar la asignación no duplica fila ni da error -- `if director not in grado.directores` decide si hay `INSERT` en `grados_directores_grado`. El selector ya excluye los dirigidos, pero el endpoint tolera que se le pida lo mismo dos veces (o que dos Admin lo hagan en paralelo desde pantallas distintas).
- **`DirectorGrado` creado bajo demanda**: la fila no existe hasta el primer nombramiento -- resolver por email y crear si no existe es exactamente el par `obtener_por_email()`/`crear()` del script, ahora en `DirectorGradoRepository`.
- **`GradoRepository.listar_disponibles_para_dirigir(director_grado_id | None)`**: `LEFT JOIN` sobre `grados_directores_grado` filtrando `IS NULL` -- mismo patrón que `listar_disponibles_para_materia()`; con `None` (el `Profesor` aún no tiene rol) devuelve todos los `Grado`. Endpoint dedicado `GET /api/v1/profesores/{id}/grados-disponibles-para-dirigir` en vez de campo embebido en el detalle: la disponibilidad cambia con cada nombramiento y la pantalla la carga fresca al montarse.
- **`200 OK` con el `Profesor` actualizado** (`ProfesorDetalleResponse` con la lista de `Grado` que dirige), no `204`: la respuesta confirma el efecto de la acción -- mismo criterio informativo que los `200` de los borrados lógicos, aquí sin cuerpo de estado que mutar.
- **`404` para `Profesor` y para `Grado` inexistentes** -- dos guardias distintas antes de tocar la asociación.
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura sobre el rol que gobierna el acceso del hilo `DirectorGrado`, explícito.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`definirDirectorGrado()` en Análisis](/RUP/02-analisis/casos-uso/definirDirectorGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/README.md) -- selector único con exclusión de los ya dirigidos.
- [`scripts/definir_director_grado.py`](/backend/app/scripts/definir_director_grado.py) -- el patrón original verificado (resolución por email + creación + añadido idempotente), ahora también como endpoint.
- [`quitarDirectorGrado()` en Diseño](/RUP/03-diseño/casos-uso/quitarDirectorGrado/README.md) -- la baja del rol, con `<<choice>>` de último director.
- [`asociarMetodologiaDocenteAAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md) -- mismo patrón de selector de disponibles + asociación idempotente.
