<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26

## Propósito

Bajada a diseño del caso de análisis [`asignarProfesorAAsignaturaGrado()`](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaGrado/README.md): sin `<<choice>>`, asignación libre exclusiva de `Admin`. Dos endpoints: el selector carga los `Profesor` disponibles (`GET .../profesores-disponibles`) y la confirmación ejecuta la asignación (`POST .../profesorado`), con el efecto colateral sobre `Guia.profesorado` resuelto dentro del mismo endpoint.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsignarProfesorAAsignaturaGradoView` (React) -- un `<select>` con los `Profesor` que la `AsignaturaGrado` todavía no tiene; al confirmar, `POST`; vuelve al detalle.
- **API**: `routers/asignatura_grado.py::listar_profesores_disponibles(asignatura_grado_id)` / `.asignar_profesor_a_asignatura_grado(asignatura_grado_id, datos)` -- `404` si la `AsignaturaGrado` o el `Profesor` no existen.
- **Modelo**: la asociación vive en la tabla M2M `asignaturas_grado_profesores` (`AsignaturaGrado.profesorado`) -- sin método de dominio propio, el router muta la colección.
- **Repositorio**: `ProfesorRepository.listar_disponibles_para_asignatura_grado(asignatura_grado_id)` (nuevo), `AsignaturaGradoRepository.asignar_profesor(asignatura_grado_id, profesor_id)` (nuevo), `GuiaRepository.obtener_por_asignatura_grado(asignatura_grado_id)` (nuevo).

## Decisiones de diseño

- **`POST /api/v1/admin/asignaturas-grado/{id}/profesorado`, namespace `/admin/`**: aunque el path sin `/admin/` (`/api/v1/asignaturas-grado/{id}/...`) no colisiona para este verbo/recurso concreto, se mantiene el namespace `/admin/` en las cuatro rutas nuevas (esta, la lista de disponibles, y las dos de `desasignarProfesorAsignaturaGrado()`) para dejar explícito que es superficie de `Admin`, no de `DirectorGrado` -- mismo criterio que las variantes Admin ya existentes de `Grado`/`Materia`/`SistemaEvaluacion`.
- **Detalle de `AsignaturaGrado` para `Admin` reutiliza `AsignaturaGradoDetalleResponse`**: mismo shape que la variante `DirectorGrado` (`GET /api/v1/asignaturas-grado/{id}`) -- se extrajo `_detalle_asignatura_grado()` como función compartida en el router para no duplicar el ensamblado. La Vista de `Admin` (`AsignaturaGradoAdmin.tsx`) solo renderiza la sección de profesorado -- las de metodologías/resultados que trae el schema no se muestran (no son gestión de `Admin`, el wireframe las marca sin enlace).
- **Efecto colateral sobre `Guia` resuelto en el mismo endpoint, atómico** (issue [#254](https://github.com/mmasias/pyCelda/issues/254), sustituye al criterio de discussion #47): el helper `_revisar_guia_por_cambio_de_profesorado(db, asignatura_grado_id)` busca la `Guia` de esa `AsignaturaGrado` (`GuiaRepository.obtener_por_asignatura_grado()`) y, **solo si está `Aprobada`**, llama a `guia.enviar_a_revision()` + añade una fila de `HistorialCambio` (`autor_id=0` centinela, comentario fijo `models.guia.COMENTARIO_REVISION_POR_PROFESORADO`). En cualquier otro estado no hace nada. **El router ya no toca `guia.profesorado` directamente.** `AsignaturaGradoRepository.asignar_profesor()`/`.desasignar_profesor()` pasan de `commit()` a `flush()` (único caller: este router) y el helper cierra la transacción una sola vez -- el cambio de plantilla y el efecto colateral se confirman juntos.
- **Reasignar un `Profesor` ya asignado es no-op**: `imparte()` se comprueba antes del `INSERT` (evita además el 500 latente por PK duplicada en la tabla M2M) y devuelve `204` sin disparar nada.
- **`204 No Content`**: mutación de una relación M2M, sin entidad que devolver -- la Vista recarga el detalle con su propio `GET`.
- **`404` para `AsignaturaGrado` y para `Profesor` inexistentes** -- dos guardias distintas antes de tocar la asociación.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`asignarProfesorAAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- el efecto colateral, cerrado en discussion #47.
- [`desasignarProfesorAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaGrado/README.md) -- la baja complementaria.
