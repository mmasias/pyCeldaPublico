<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearReferenciaBibliografica() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearReferenciaBibliografica/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearReferenciaBibliografica()`](/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/README.md): CRUD real e inmediato contra `ReferenciaBibliograficaRepository`, sin ninguna interacción con `Guia` ni con capa Service. Un único paso, sin `<<choice>>` -- `ReferenciaBibliografica` no tiene ninguna regla de negocio documentada en el modelo de dominio, así que la obligatoriedad de `tipo`/`referencia` se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia.

**Retocado (issue #226, 2026-09-05)**: `tipo` pasa de `str` libre a un `Literal` cerrado de los cuatro valores-enum ya fijados en [Modelo](/RUP/00-modelo-del-dominio/README.md) (`Basica`/`Complementaria`/`WebsReferencia`/`OtrasFuentes`) -- Modelo y Análisis ya lo describían como "enum cerrado", pero nunca llegó a materializarse en Pydantic, así que hasta ahora cualquier string pasaba (convivían en producción `"Básica"`/`"Complementaria"`/`"Web"` del seed con las cuatro etiquetas del frontend, sin que ninguno de los dos vocabularios fuera el válido). Mismo mecanismo que `TipoSesion` (`schemas/sesion.py`): `Literal` en el schema, columna sigue `String(30)` sin enum de esquema.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearReferenciaBibliograficaView` (React) -- formulario mínimo (`tipo`, `referencia`); al confirmar, `POST /api/v1/guias/{guia_id}/referencias-bibliograficas`.
- **API**: `routers/referencia_bibliografica.py::crear_referencia_bibliografica(guia_id, datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `ReferenciaBibliografica` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente a partir de los campos del formulario, no hay método de dominio que llamar.
- **Repositorio**: `ReferenciaBibliograficaRepository.crear(guia_id, tipo, referencia)` -- persistencia real e inmediata, no una mutación de sesión.

## Decisiones de diseño

- **Sin capa Service**: la función del Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `ReferenciaBibliograficaCreate` (Pydantic) exige `tipo`/`referencia` antes de que la función del Router se ejecute -- mismo mecanismo que el `AulaCreate` de referencia en pySigHor.
- **La fila nace con `guia_id` pero sin vincular**: pertenece a esta `Guia` desde su creación (columna `guia_id` fija), pero su vinculación a la colección oficial (`vinculada: bool`, default `False`) es responsabilidad de [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- decisión 1 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58), no de este endpoint.
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista navega de inmediato a `editarReferenciaBibliografica()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id`.
- **La Vista mapea valor-enum <-> etiqueta legible, el dato persistido es el valor-enum**: el `<select>` de `CrearReferenciaBibliograficaView` ofrece las cuatro etiquetas ("Básica", "Complementaria", "Webs de referencia", "Otras fuentes de consulta") pero envía el valor-enum correspondiente en el `POST` -- ya lo exigía Requisitos (los wireframes de [`abrirReferenciasBibliograficas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/wireframes.puml) muestran siempre la etiqueta, nunca el valor-enum crudo), pero antes de este retoque no había ningún valor-enum que mapear -- el dato crudo y la etiqueta eran la misma cosa.

## Referencias

- [`crearReferenciaBibliografica()` en Análisis](/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/README.md).
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- decisión original del enum de cuatro valores, nunca materializada hasta este retoque.
- [`editarReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md) -- mismo `Literal`, mismo mapeo de Vista.
