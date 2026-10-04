<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > rechazarGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/rechazarGuia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`rechazarGuia()`](/RUP/02-analisis/casos-uso/rechazarGuia/README.md): `POST /api/v1/guias/{guia_id}/rechazar`, mismo patrón de tres piezas que [`aprobarGuia()`](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) (transición de estado, registro de historial, persistencia), pero con `comentario` opcional transportado en el body en vez de fijo por el propio Router.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/rechazarGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `RechazarGuiaView` (React) -- recoge el `comentario` opcional; pide `POST /api/v1/guias/{guia_id}/rechazar`.
- **API**: `routers/guia.py::rechazar_guia(guia_id, datos)` -- función nueva; coordina transición, historial y persistencia.
- **Modelo**: `Guia.rechazar()` -- aplica `EnRevision -> Rechazada`; `HistorialCambio.registrar(campo, valorAnterior, valorNuevo, comentario)` -- con el `comentario` recibido del actor.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`.

## Decisiones de diseño

- **Mismo esqueleto que `aprobarGuia()`**: obtener, transicionar, registrar historial, persistir -- la única diferencia real es que el `comentario` viaja en el `RechazarGuiaRequest` (Pydantic) en vez de ser una cadena fija del Router.
- **Sin `alt` de negocio**: la especificación no modela rama de fallo -- la acción solo es alcanzable sobre una `Guia` `EnRevision` (el botón condicional de la Vista ya lo garantiza).
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **Autenticación fuera de este diagrama**: el `director_programa_id` llega inyectado por *dependency override*, mismo criterio que el resto de la rebanada.

## Referencias

- [`rechazarGuia()` en Análisis](/RUP/02-analisis/casos-uso/rechazarGuia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/README.md).
- [`aprobarGuia()` en Diseño](/RUP/03-diseño/casos-uso/aprobarGuia/README.md) -- mismo esqueleto de tres piezas, comentario fijo en vez de recibido.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `EnRevision -> Rechazada`.
