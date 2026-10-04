<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26

## Propósito

Bajada a diseño del caso de análisis [`asignarProfesorAAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/README.md): sin `<<choice>>`, asignación libre exclusiva de `Admin`. Dos endpoints: el selector carga los `Profesor` disponibles (`GET .../profesores-disponibles`) y la confirmación ejecuta la asignación (`POST .../profesorado`), con el efecto colateral sobre `Guia.profesorado` resuelto dentro del mismo endpoint.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsignarProfesorAAsignaturaProgramaView` (React) -- un `<select>` con los `Profesor` que la `AsignaturaPrograma` todavía no tiene; al confirmar, `POST`; vuelve al detalle.
- **API**: `routers/asignatura_programa.py::listar_profesores_disponibles(asignatura_programa_id)` / `.asignar_profesor_a_asignatura_programa(asignatura_programa_id, datos)` -- `404` si la `AsignaturaPrograma` o el `Profesor` no existen.
- **Modelo**: la asociación vive en la tabla M2M `asignaturas_programa_profesores` (`AsignaturaPrograma.profesorado`) -- sin método de dominio propio, el router muta la colección.
- **Repositorio**: `ProfesorRepository.listar_disponibles_para_asignatura_programa(asignatura_programa_id)` (nuevo), `AsignaturaProgramaRepository.asignar_profesor(asignatura_programa_id, profesor_id)` (nuevo), `GuiaRepository.obtener_por_asignatura_programa(asignatura_programa_id)` (nuevo).

## Decisiones de diseño

- **`POST /api/v1/admin/asignaturas-programa/{id}/profesorado`, namespace `/admin/`**: aunque el path sin `/admin/` (`/api/v1/asignaturas-programa/{id}/...`) no colisiona para este verbo/recurso concreto, se mantiene el namespace `/admin/` en las cuatro rutas nuevas (esta, la lista de disponibles, y las dos de `desasignarProfesorAsignaturaPrograma()`) para dejar explícito que es superficie de `Admin`, no de `DirectorPrograma` -- mismo criterio que las variantes Admin ya existentes de `Programa`/`Materia`/`SistemaEvaluacion`.
- **Detalle de `AsignaturaPrograma` para `Admin` reutiliza `AsignaturaProgramaDetalleResponse`**: mismo shape que la variante `DirectorPrograma` (`GET /api/v1/asignaturas-programa/{id}`) -- se extrajo `_detalle_asignatura_programa()` como función compartida en el router para no duplicar el ensamblado. La Vista de `Admin` (`AsignaturaProgramaAdmin.tsx`) solo renderiza la sección de profesorado -- las de metodologías/resultados que trae el schema no se muestran (no son gestión de `Admin`, el wireframe las marca sin enlace).
- **Efecto colateral sobre `Guia` resuelto en el mismo endpoint, atómico** (issue [#254](https://github.com/mmasias/pyCelda/issues/254), sustituye al criterio de discussion #47): el helper `_revisar_guia_por_cambio_de_profesorado(db, asignatura_programa_id)` busca la `Guia` de esa `AsignaturaPrograma` (`GuiaRepository.obtener_por_asignatura_programa()`) y, **solo si está `Aprobada`**, llama a `guia.enviar_a_revision()` + añade una fila de `HistorialCambio` (`autor_id=0` centinela, comentario fijo `models.guia.COMENTARIO_REVISION_POR_PROFESORADO`). En cualquier otro estado no hace nada. **El router ya no toca `guia.profesorado` directamente.** `AsignaturaProgramaRepository.asignar_profesor()`/`.desasignar_profesor()` pasan de `commit()` a `flush()` (único caller: este router) y el helper cierra la transacción una sola vez -- el cambio de plantilla y el efecto colateral se confirman juntos.
- **Reasignar un `Profesor` ya asignado es no-op**: `imparte()` se comprueba antes del `INSERT` (evita además el 500 latente por PK duplicada en la tabla M2M) y devuelve `204` sin disparar nada.
- **`204 No Content`**: mutación de una relación M2M, sin entidad que devolver -- la Vista recarga el detalle con su propio `GET`.
- **`404` para `AsignaturaPrograma` y para `Profesor` inexistentes** -- dos guardias distintas antes de tocar la asociación.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`asignarProfesorAAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/README.md) -- el efecto colateral, cerrado en discussion #47.
- [`desasignarProfesorAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaPrograma/README.md) -- la baja complementaria.
