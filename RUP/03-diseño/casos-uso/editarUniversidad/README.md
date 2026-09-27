<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarUniversidad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarUniversidad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarUniversidad()`](/RUP/02-analisis/casos-uso/editarUniversidad/README.md): CRUD real e inmediato, `PUT /api/v1/universidades/{universidad_id}`, sin ninguna llamada a otra entidad. A diferencia de `editarPonderacionEvaluacion()`, sin `alt` de negocio -- solo la validación de forma que Pydantic ya resuelve. `Universidad` gana aquí su método `actualizar(nombre)`, simétrico a `ReferenciaBibliografica.actualizar(tipo, referencia)`. Es también el destino del `<<include>>` de `crearUniversidad()`: tras crear, el `Admin` queda editando la `Universidad` recién creada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarUniversidad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarUniversidadView` (React) -- carga el formulario con `GET /api/v1/universidades/{universidad_id}` (mismo endpoint que `abrirUniversidad()`), envía cambios con `PUT`.
- **API**: `routers/universidad.py::editar_universidad(universidad_id, datos)` -- función nueva; sin validación de negocio, solo coordina la actualización.
- **Modelo**: `Universidad.actualizar(nombre)` -- método nuevo, mismo patrón que `ReferenciaBibliografica.actualizar(tipo, referencia)`.
- **Repositorio**: `UniversidadRepository.obtener(universidad_id)` (reutilizado); `.actualizar(universidad)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio, a diferencia de `editarPonderacionEvaluacion()`**: `Universidad` no tiene ninguna regla de validación cruzada en el modelo de dominio -- la única validación es de forma (`nombre` obligatorio), resuelta por `UniversidadUpdate` (Pydantic), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`.
- **`UniversidadRepository.actualizar(universidad)` es método nuevo**: el repositorio nace en esta rebanada con `listar`/`obtener`/`crear`/`actualizar`, completo para los cuatro CU de `Universidad`.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **Reutiliza el `GET` de `abrirUniversidad()`**: mismo endpoint de carga, sin duplicar lógica de lectura.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/universidad.py` debe declararla explícitamente en Desarrollo. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`editarUniversidad()` en Análisis](/RUP/02-analisis/casos-uso/editarUniversidad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/README.md).
- [`abrirUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) -- mismo endpoint `GET`, reutilizado.
- [`crearUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/crearUniversidad/README.md) -- `<<include>>` de origen.
- [`editarReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio.
