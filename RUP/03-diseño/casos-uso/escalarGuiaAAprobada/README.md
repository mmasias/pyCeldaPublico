<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > escalarGuiaAAprobada() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/README.md)|[Análisis](/RUP/02-analisis/casos-uso/escalarGuiaAAprobada/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/escalarGuiaAAprobada/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`escalarGuiaAAprobada()`](/RUP/02-analisis/casos-uso/escalarGuiaAAprobada/README.md): `POST /api/v1/guias/{guia_id}/escalar-a-aprobada`, sin formulario, mismo criterio de comentario fijo que [`aprobarGuia()`](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- la diferencia real es que el estado de origen no es único (`{Borrador, Rechazada}`), así que `Guia.escalar_a_aprobada()` devuelve el estado real de partida para que el `HistorialCambio` lo registre correctamente.

**Retoque posterior (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224), cierre de Frente B)**: mismo retoque que [`aprobarGuia()`](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- `escalar_a_aprobada()` gana una línea más en su propio cuerpo, `self.regenerar_pdf()`, tras fijar `estado = "Aprobada"`. El Router no cambia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/escalarGuiaAAprobada/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EscalarGuiaAAprobadaView` (React) -- recoge la solicitud sin pedir ningún dato; pide `POST /api/v1/guias/{guia_id}/escalar-a-aprobada`.
- **API**: `routers/guia.py::escalar_guia_a_aprobada(guia_id)` -- función nueva; coordina transición, historial y persistencia.
- **Modelo**: `Guia.escalar_a_aprobada()` -- aplica `{Borrador, Rechazada} -> Aprobada`, llama a `self.regenerar_pdf()` (retoque posterior, discussion #224) y devuelve el estado real de origen; `HistorialCambio.registrar(...)` con comentario fijo `"escalada a aprobada sin incidencia"`.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`.

## Decisiones de diseño

- **`Guia.escalar_a_aprobada()` devuelve el estado de origen**: a diferencia de `Guia.aprobar()` (origen fijo `EnRevision`), aquí el Router necesita saber si venía de `Borrador` o `Rechazada` para pasarlo a `HistorialCambio.registrar()` -- el método del Modelo lo devuelve en vez de que el Router lo infiera aparte.
- **Comentario fijo por el Router**, no por el actor: mismo criterio que `aprobarGuia()`, sin campo de formulario.
- **Sin `alt` de negocio**: la acción solo es alcanzable sobre `Guia` `Borrador`/`Rechazada` -- el botón condicional de la Vista ya lo garantiza, mismo criterio que `aprobarGuia()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **`regenerar_pdf()` como self-call dentro de `escalar_a_aprobada()`**: mismo criterio que [`aprobarGuia()`](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- consecuencia directa e incondicional del propio cambio de estado, encapsulada en el método.
- **`_sincronizar_profesorado()` como segundo self-call** (issue [#254](https://github.com/mmasias/pyCelda/issues/254)): idéntico a `aprobarGuia()` -- un escalado directo a `Aprobada` también re-deriva `Guia -- Profesor` de la plantilla.

## Referencias

- [`escalarGuiaAAprobada()` en Análisis](/RUP/02-analisis/casos-uso/escalarGuiaAAprobada/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/README.md).
- [`aprobarGuia()` en Diseño](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- mismo criterio de comentario fijo, origen único en vez de doble; mismo retoque de `regenerar_pdf()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `{Borrador, Rechazada} -> Aprobada`.
- [`editarSemestreGuia()` en Diseño](/RUP/03-diseño/casos-uso/editarSemestreGuia/README.md) -- disparador original de `regenerar_pdf()`, ya no en exclusiva.
- Discussion [#224](https://github.com/mmasias/pyCelda/discussions/224) -- cierre de Frente B.
