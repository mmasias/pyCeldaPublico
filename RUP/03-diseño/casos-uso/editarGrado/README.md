<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarGrado()`](/RUP/02-analisis/casos-uso/editarGrado/README.md): CRUD real e inmediato, `PUT /api/v1/admin/grados/{grado_id}`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- `Grado` no tiene ninguna regla de validación cruzada en el modelo de dominio; la única validación es de forma (`nombre` obligatorio), resuelta por Pydantic. `estado` queda fuera del formulario: se gestiona en exclusiva desde [`eliminarGrado()`](/RUP/03-diseño/casos-uso/eliminarGrado/README.md). `Grado` gana aquí su método `actualizar(nombre)`. Es también el destino del `<<include>>` de `crearGrado()`: tras crear, el `Admin` queda editando el `Grado` recién creado.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarGradoView` (React) -- carga el formulario con `GET /api/v1/admin/grados/{grado_id}` (endpoint propio de Admin, no el `GET /api/v1/grados/{grado_id}` de `DirectorGrado`, que además agrega la tabla de `AsignaturaGrado`); envía cambios con `PUT`; el formulario presenta `codigo` como texto plano de solo lectura (no un `<input>` deshabilitado) y nunca presenta `estado`.
- **API**: `routers/grado.py::obtener_grado_admin(grado_id)` / `editar_grado(grado_id, datos)` -- funciones nuevas; sin validación de negocio, solo coordinan la actualización. El sufijo `_admin` en `obtener_grado_admin` evita colisionar de nombre con `obtener_grado()` ya existente (variante `DirectorGrado`).
- **Modelo**: `Grado.actualizar(nombre)` -- método nuevo, mismo patrón que `Asignatura.actualizar(nombre, ects, contenido)`.
- **Repositorio**: `GradoRepository.obtener(grado_id)` (reutilizado); `.actualizar(grado)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio**: `Grado` no tiene ninguna regla de validación cruzada en el modelo de dominio -- la única validación es de forma, resuelta por `GradoUpdate` (Pydantic: `nombre` obligatorio), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`. `estado` no viaja en el esquema: la edición no puede mutarlo.
- **`codigo` no viaja en `GradoUpdate` -- el único campo mutable es `nombre`**: diferencia real frente a `editarAsignatura()`/`editarUniversidad()`, que sí editan su campo "clave". El `codigo` se muestra en el formulario pero como solo lectura (Requisitos: "El código no es editable una vez creado el Grado") -- es un identificador real usado fuera del propio nombre (URLs, nomenclatura de ficheros del corpus, discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)), y su inmutabilidad se garantiza por ausencia del esquema, no por confiar en que la Vista lo envíe intacto.
- **`GradoRepository.actualizar(grado)` es método nuevo**: el repositorio nació con `obtener`/`listar_dirigidos_por`; `actualizar` lo introduce esta rebanada y lo reutiliza también `eliminarGrado()` para persistir el `Extinguido`.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **Nada cambia de rutas en esta corrección**: `GET`/`PUT /api/v1/admin/grados/{grado_id}` siguen operando por `grado_id` suelto, ya no dependen del listado. Solo la navegación de vuelta se ajusta al listado anidado. Corregido tras revisión en vivo de Manuel -- el wireframe real de `abrirGrados()` (`GRADOS -- ESCUELA POLITÉCNICA SUPERIOR`) y el Objetivo de `crearGrado()` ("en el catálogo de una Facultad") exigen listado/creación anidados bajo `Facultad`, no un listado global -- verificado contra el wireframe antes de corregir. El "volver" tras guardar/cancelar navega al detalle del `Grado` (`/admin/grados/{grado_id}`) y de ahí al listado `/facultades/{facultad_id}/grados` (vía el `facultad_id` que `GradoResponse` ahora expone); si el `Grado` es legado sin Facultad, se cae a `/panel-administracion`.

## Referencias

- [`editarGrado()` en Análisis](/RUP/02-analisis/casos-uso/editarGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/README.md).
- [`crearGrado()` en Diseño](/RUP/03-diseño/casos-uso/crearGrado/README.md) -- `<<include>>` de origen.
- [`abrirGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirGrado/README.md) -- el `GET` de `DirectorGrado`, mismo repositorio, endpoint distinto y con agregado de `AsignaturaGrado`.
- [`eliminarGrado()` en Diseño](/RUP/03-diseño/casos-uso/eliminarGrado/README.md) -- único gestor del `estado`, fuera de este formulario.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio.
