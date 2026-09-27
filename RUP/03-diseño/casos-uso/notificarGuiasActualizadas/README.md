<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > notificarGuiasActualizadas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/notificarGuiasActualizadas/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`notificarGuiasActualizadas()`](/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/README.md): `POST /api/v1/grados/{grado_id}/notificar-guias-actualizadas`, sin Modelo ni Repository -- mismo criterio que Análisis, el mecanismo de envío (email, log, cola de mensajería) es infraestructura fuera del alcance de este diagrama y de esta rebanada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/notificarGuiasActualizadas/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `NotificarGuiasActualizadasView` (React) -- pide `POST /api/v1/grados/{grado_id}/notificar-guias-actualizadas`.
- **API**: `routers/guia.py::notificar_guias_actualizadas(grado_id)` -- función nueva; dispara el aviso, sin tocar base de datos.
- **Modelo**: ninguno.
- **Repositorio**: ninguno.

## Decisiones de diseño

- **Sin Base de Datos**: único endpoint de todo el catálogo de Diseño (9+12 casos) que no toca `DB` en absoluto -- ni lectura ni escritura. Mismo nivel de abstracción que Análisis, que ya lo dejó sin ninguna clase de Modelo.
- **Mecanismo de envío real, fuera de alcance**: el `secuencia.puml` documenta el disparo como una nota interna del Router (`API -> API`), sin comprometerse con SMTP/cola/lo que sea -- esa decisión de implementación se toma en Desarrollo, si y cuando este endpoint se construya de verdad.
- **`routers/guia.py`, no un router nuevo**: mismo criterio que `consultarEstadoGuias()` -- el dominio que se notifica es `Guia`, aunque la URL cuelgue de `/grados/{grado_id}`.
- **Sin capa Service**: no aplica de forma directa (no hay lógica de negocio que orquestar), pero se documenta por consistencia.

## Referencias

- [`notificarGuiasActualizadas()` en Análisis](/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/README.md) -- diagrama de colaboración origen, ya sin ninguna clase de Modelo.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- mismo `:GUIAS_DEL_GRADO_ABIERTO` sobre el que este caso hace self-loop.
