<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarReferenciaBibliografica() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/editarReferenciaBibliografica/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarReferenciaBibliografica()`](/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/README.md): CRUD real e inmediato, `PUT /api/v1/referencias-bibliograficas/{referencia_id}`, sin ninguna llamada a `Guia`. A diferencia de [`editarPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md), sin `alt` de negocio -- solo la validación de forma que Pydantic ya resuelve (decisión de la discussion #60, ver diagrama de clases). Cierra la asimetría señalada en el diagrama de clases de Diseño: `ReferenciaBibliografica` gana su método `actualizar()`, simétrico a `PonderacionEvaluacion.actualizar()`.

**Retocado (issue #226, 2026-09-05)**: `tipo` pasa de `str` libre a un `Literal` cerrado de los cuatro valores-enum ya fijados en [Modelo](/RUP/00-modelo-del-dominio/README.md) (`Basica`/`Complementaria`/`WebsReferencia`/`OtrasFuentes`) -- ver el mismo retoque en [`crearReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarReferenciaBibliograficaView` (React) -- carga el formulario con `GET /api/v1/referencias-bibliograficas/{referencia_id}` (mismo endpoint que `abrirReferenciaBibliografica()`), envía cambios con `PUT`.
- **API**: `routers/referencia_bibliografica.py::editar_referencia_bibliografica(referencia_id, datos)` -- función nueva; sin validación de negocio, solo coordina la actualización.
- **Modelo**: `ReferenciaBibliografica.actualizar(tipo, referencia)` -- método nuevo, cierra la asimetría con `PonderacionEvaluacion.actualizar()`.
- **Repositorio**: `ReferenciaBibliograficaRepository.obtener(referencia_id)` (reutilizado); `.actualizar(referencia)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio, a diferencia de `editarPonderacionEvaluacion()`**: `ReferenciaBibliografica` no tiene ninguna regla de validación cruzada en el modelo de dominio -- la única validación es de forma (`tipo`/`referencia` obligatorios), resuelta por `ReferenciaBibliograficaUpdate` (Pydantic), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`.
- **`ReferenciaBibliograficaRepository.actualizar(referencia)` es método nuevo**: hasta ahora el repositorio solo tenía `crear`/`listar_vinculadas_de`/`listar_pendientes_de`/`existe_pendiente_de`/`vincular`/`desvincular` -- sin `actualizar`, porque ningún caso de uso construido lo necesitaba.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **Reutiliza el GET de `abrirReferenciaBibliografica()`**: mismo endpoint de carga, sin duplicar lógica de lectura.
- **Mismo mapeo valor-enum <-> etiqueta que `crearReferenciaBibliografica()`**: el `<select>` precarga la etiqueta correspondiente al valor-enum actual (`GET` devuelve el valor-enum crudo), y el `PUT` envía de vuelta el valor-enum seleccionado.

## Referencias

- [`editarReferenciaBibliografica()` en Análisis](/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/README.md).
- [`abrirReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/abrirReferenciaBibliografica/README.md) -- mismo endpoint GET, reutilizado.
- [`editarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- contraste: sí tiene `alt` de negocio (máximo del `SistemaEvaluacion`), este caso no.
- [Diagrama de clases de Diseño](/RUP/03-diseño/diagrama-clases-diseño.puml) -- nota sobre `ReferenciaBibliografica` sin métodos propios, resuelta en este caso de uso.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- decisión original del enum de cuatro valores, nunca materializada hasta este retoque.
- [`crearReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md) -- mismo `Literal`, mismo mapeo de Vista.
