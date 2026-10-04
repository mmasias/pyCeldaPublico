<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirReferenciasBibliograficas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirReferenciasBibliograficas/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirReferenciasBibliograficas()`](/RUP/02-analisis/casos-uso/abrirReferenciasBibliograficas/README.md): simétrico a [`abrirPonderacionesEvaluacion()`](/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/README.md), sobre `ReferenciaBibliografica`. Un único endpoint de lectura, sin capa Service, fusiona vinculadas + pendientes.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirReferenciasBibliograficas/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirReferenciasBibliograficasView` (React) -- pide `GET /api/v1/guias/{guia_id}/referencias-bibliograficas`.
- **API**: `routers/referencia_bibliografica.py::listar_referencias_bibliograficas(guia_id)` -- función suelta; obtiene la `Guia`, lista vinculadas y pendientes, y fusiona.
- **Modelo**: `Guia` -- sin lógica propia invocada.
- **Repositorio**: `GuiaRepository.obtener(guia_id)`; `ReferenciaBibliograficaRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)` -- mismos métodos ya usados por `abrirGuia()`.

## Decisiones de diseño

- **Fusión en el Router, no en `Guia`**: mismo criterio que `abrirGuia()`/`abrirPonderacionesEvaluacion()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository directamente.
- **Segundo endpoint real del módulo `referencia_bibliografica.py`**: hasta este lote, ese router solo tenía `crear_referencia_bibliografica` (los 9 originales) -- este caso de uso lo amplía sin tocar la función existente.
- **Autenticación fuera de este diagrama**: mismo criterio que el resto de la rebanada.

## Referencias

- [`abrirReferenciasBibliograficas()` en Análisis](/RUP/02-analisis/casos-uso/abrirReferenciasBibliograficas/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/README.md).
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- mismo mecanismo de fusión.
- [`abrirPonderacionesEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/README.md) -- caso simétrico, sobre `PonderacionEvaluacion`.
