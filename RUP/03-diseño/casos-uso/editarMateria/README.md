<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarMateria()`](/RUP/02-analisis/casos-uso/editarMateria/README.md): CRUD real e inmediato, `PUT /api/v1/admin/materias/{materia_id}`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- `Materia` no tiene ninguna regla de validación cruzada en el modelo de dominio; la única validación es de forma (`nombre` obligatorio), resuelta por Pydantic. `Materia` gana aquí su método `actualizar(nombre)`. Es también el destino del `<<include>>` de `crearMateria()`: tras crear, el `Admin` queda editando la `Materia` recién creada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarMateriaAdmin.tsx` (React, ruta `/admin/materias/{materia_id}/editar`) -- carga el formulario con `GET /api/v1/admin/materias/{materia_id}` (endpoint Admin de la variante reducida de `abrirMateria()`, no el `GET /api/v1/materias/{materia_id}` de `DirectorGrado`, que agrega las colecciones de asociación); envía cambios con `PUT`.
- **API**: `routers/materia.py::obtener_materia_admin(materia_id)` / `editar_materia(materia_id, datos)` -- funciones nuevas; sin validación de negocio, solo coordinan la actualización. El sufijo `_admin` evita colisionar de nombre con `obtener_materia()` ya existente (variante `DirectorGrado`).
- **Modelo**: `Materia.actualizar(nombre)` -- método nuevo, mismo patrón que `Grado.actualizar(nombre)`/`Universidad.actualizar(nombre)`.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` (reutilizado); `.actualizar(materia)` -- método nuevo, mismo perfil que `GradoRepository.actualizar(grado)`.

## Decisiones de diseño

- **Sin `alt` de negocio**: la única validación es de forma, resuelta por `MateriaUpdate` (Pydantic: `nombre` obligatorio), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`. Sin `estado` que gestionar: `Materia` no se extingue.
- **El `GET` previo usa el endpoint Admin reducido**: `MateriaAdminDetalleResponse` solo agrega `asignaturas_grado` -- suficiente para el formulario (que solo pinta `nombre`) y sin pedir las colecciones de asociación que `DirectorGrado` usa y `Admin` no.
- **Namespace `/api/v1/admin/materias/{materia_id}`, con `Depends(require_admin)`** -- separado del `/api/v1/materias/{materia_id}` de `DirectorGrado`, mismo criterio del resto del namespace Admin. Especialmente relevante por ser endpoint de escritura (IDOR #86/#96).
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Sin capa Service**: Router delgado -> Modelo/Repository.

## Referencias

- [`editarMateria()` en Análisis](/RUP/02-analisis/casos-uso/editarMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/README.md).
- [`crearMateria()` en Diseño](/RUP/03-diseño/casos-uso/crearMateria/README.md) -- `<<include>>` de origen.
- [`editarGrado()` en Diseño](/RUP/03-diseño/casos-uso/editarGrado/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio, el precedente directo de la rebanada anterior.
- [`abrirMateria()` en Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md) -- el `GET` de la variante Admin reducida, construido en este mismo lote.
