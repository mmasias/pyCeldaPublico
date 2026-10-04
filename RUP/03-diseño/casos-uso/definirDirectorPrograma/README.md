<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > definirDirectorPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/definirDirectorPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`definirDirectorPrograma()`](/RUP/02-analisis/casos-uso/definirDirectorPrograma/README.md): alta del rol `DirectorPrograma` sobre un `Profesor` ya abierto, sin `<<choice>>` (cardinalidad muchos a muchos libre, discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)). Dos endpoints: el selector carga los `Programa` disponibles (`GET .../programas-disponibles-para-dirigir`) y la confirmación ejecuta la asignación (`POST .../directores-programa`). El mecanismo replica el patrón verificado de `app/scripts/definir_director_programa.py` (que queda como herramienta de operación manual, superseded sin conflicto): resolver el `DirectorPrograma` por email -- creándolo si no existía -- e añadir el `Programa` si no estaba ya.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/definirDirectorPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DefinirDirectorProgramaView` (React) -- un `<select>` con los `Programa` que el `Profesor` todavía no dirige (`codigo -- nombre`); al confirmar, `POST`; vuelve al detalle.
- **API**: `routers/profesor.py::listar_programas_disponibles_para_dirigir(profesor_id)` / `.definir_director_programa(profesor_id, datos)` -- `404` si el `Profesor` o el `Programa` no existen.
- **Modelo**: la asociación vive en la tabla M2M `programas_directores_programa` (`Programa.directores`) -- sin método de dominio propio; el router muta la colección.
- **Repositorio**: `DirectorProgramaRepository.obtener_por_email()` / `.crear(email)` (resolución del rol con creación bajo demanda), `ProgramaRepository.listar_disponibles_para_dirigir(director_programa_id | None)` (nuevo) / `.obtener()`, `ProfesorRepository.obtener()`.

## Decisiones de diseño

- **Idempotente, mismo criterio que el script CLI**: reejecutar la asignación no duplica fila ni da error -- `if director not in programa.directores` decide si hay `INSERT` en `programas_directores_programa`. El selector ya excluye los dirigidos, pero el endpoint tolera que se le pida lo mismo dos veces (o que dos Admin lo hagan en paralelo desde pantallas distintas).
- **`DirectorPrograma` creado bajo demanda**: la fila no existe hasta el primer nombramiento -- resolver por email y crear si no existe es exactamente el par `obtener_por_email()`/`crear()` del script, ahora en `DirectorProgramaRepository`.
- **`ProgramaRepository.listar_disponibles_para_dirigir(director_programa_id | None)`**: `LEFT JOIN` sobre `programas_directores_programa` filtrando `IS NULL` -- mismo patrón que `listar_disponibles_para_materia()`; con `None` (el `Profesor` aún no tiene rol) devuelve todos los `Programa`. Endpoint dedicado `GET /api/v1/profesores/{id}/programas-disponibles-para-dirigir` en vez de campo embebido en el detalle: la disponibilidad cambia con cada nombramiento y la pantalla la carga fresca al montarse.
- **`200 OK` con el `Profesor` actualizado** (`ProfesorDetalleResponse` con la lista de `Programa` que dirige), no `204`: la respuesta confirma el efecto de la acción -- mismo criterio informativo que los `200` de los borrados lógicos, aquí sin cuerpo de estado que mutar.
- **`404` para `Profesor` y para `Programa` inexistentes** -- dos guardias distintas antes de tocar la asociación.
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura sobre el rol que gobierna el acceso del hilo `DirectorPrograma`, explícito.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`definirDirectorPrograma()` en Análisis](/RUP/02-analisis/casos-uso/definirDirectorPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/README.md) -- selector único con exclusión de los ya dirigidos.
- `scripts/definir_director_programa.py` -- el patrón original verificado (resolución por email + creación + añadido idempotente), ahora también como endpoint.
- [`quitarDirectorPrograma()` en Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md) -- la baja del rol, con `<<choice>>` de último director.
- [`asociarMetodologiaDocenteAAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- mismo patrón de selector de disponibles + asociación idempotente.
