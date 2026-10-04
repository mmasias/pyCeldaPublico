<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirReferenciaBibliografica() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirReferenciaBibliografica/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirReferenciaBibliografica()`](/RUP/02-analisis/casos-uso/abrirReferenciaBibliografica/README.md): primer caso de la rebanada que necesita leer una `ReferenciaBibliografica` individual -- introduce el endpoint `GET /api/v1/referencias-bibliograficas/{referencia_id}` y el método `ReferenciaBibliograficaRepository.obtener(referencia_id)`, ninguno de los dos existía hasta ahora (`crearReferenciaBibliografica()`/`eliminarReferenciaBibliografica()` no los necesitaban). Reutilizado después por [`editarReferenciaBibliografica()`](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirReferenciaBibliografica/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirReferenciaBibliograficaView` (React) -- pide `GET /api/v1/referencias-bibliograficas/{referencia_id}`, sin edición.
- **API**: `routers/referencia_bibliografica.py::obtener_referencia_bibliografica(referencia_id)` -- función nueva, reutilizada después por `editar_referencia_bibliografica`.
- **Modelo**: ninguno con lógica propia invocada.
- **Repositorio**: `ReferenciaBibliograficaRepository.obtener(referencia_id)` -- método nuevo.

## Decisiones de diseño

- **Endpoint y método de repositorio nuevos, simétricos a `PonderacionEvaluacionRepository.obtener()`**: hasta ahora `ReferenciaBibliograficaRepository` no tenía lectura individual porque ningún caso de uso la necesitaba (`crear`/`eliminar` trabajan con los datos que ya traen).
- **Sin capa Service**: función suelta en el Router.
- **Autenticación fuera de este diagrama**: mismo criterio que el resto de la rebanada.

## Referencias

- [`abrirReferenciaBibliografica()` en Análisis](/RUP/02-analisis/casos-uso/abrirReferenciaBibliografica/README.md) -- diagrama de colaboración origen, introduce `cargarReferenciaBibliografica(referenciaId)`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/README.md).
- [`editarReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md) -- reutiliza este mismo endpoint para cargar el formulario.
- [`abrirPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionEvaluacion/README.md) -- caso simétrico, pero ahí el endpoint ya existía (reutilizado de `editarPonderacionEvaluacion()`).
