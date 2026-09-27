<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > revocarAprobacionGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/revocarAprobacionGuia/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/revocarAprobacionGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`revocarAprobacionGuia()`](/RUP/02-analisis/casos-uso/revocarAprobacionGuia/README.md): `POST /api/v1/guias/{guia_id}/revocar-aprobacion`, misma forma que [`rechazarGuia()`](/RUP/03-diseño/casos-uso/rechazarGuia/README.md) -- comentario opcional en el body, transición `Aprobada -> Borrador`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/revocarAprobacionGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `RevocarAprobacionGuiaView` (React) -- recoge el `comentario` opcional; pide `POST /api/v1/guias/{guia_id}/revocar-aprobacion`.
- **API**: `routers/guia.py::revocar_aprobacion_guia(guia_id, datos)` -- función nueva; coordina transición, historial y persistencia.
- **Modelo**: `Guia.revocar_aprobacion()` -- aplica `Aprobada -> Borrador`; `HistorialCambio.registrar(...)` con el `comentario` recibido.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`.

## Decisiones de diseño

- **Mismo esqueleto que `rechazarGuia()`**: comentario opcional transportado en `RevocarAprobacionGuiaRequest` (Pydantic).
- **Sin `alt` de negocio**: la acción solo es alcanzable sobre `Guia` `Aprobada` -- botón condicional de la Vista.
- **Sin capa Service**: Router delgado -> Modelo/Repository.

## Referencias

- [`revocarAprobacionGuia()` en Análisis](/RUP/02-analisis/casos-uso/revocarAprobacionGuia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/README.md).
- [`rechazarGuia()` en Diseño](/RUP/03-diseño/casos-uso/rechazarGuia/README.md) -- misma forma, comentario opcional.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `Aprobada -> Borrador` (revocación).
