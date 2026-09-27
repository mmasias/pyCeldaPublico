<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirResultadoAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirResultadoAprendizaje()`](/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Recupera un `ResultadoAprendizaje` por identificador para presentarlo en detalle -- mismo patrón de lectura simple que `abrirPonderacionEvaluacion()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirResultadoAprendizaje/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirResultadoAprendizajeView` (React) -- pide `GET /api/v1/resultados-aprendizaje/{resultado_aprendizaje_id}`; muestra `codigo`, `tipo`, `descripcion`.
- **API**: `routers/resultado_aprendizaje.py::obtener_resultado_aprendizaje(resultado_aprendizaje_id)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- `ResultadoAprendizaje` solo porta los datos presentados.
- **Repositorio**: `ResultadoAprendizajeRepository.obtener(resultado_aprendizaje_id)` -- `SELECT` por identificador.

## Decisiones de diseño

- **Endpoint propio, no reutilizado**: a diferencia de `abrirPonderacionEvaluacion()` (que reutilizaba el de `editarPonderacionEvaluacion()` porque el PUT ya devolvía la entidad), aquí no existe un endpoint previo de `ResultadoAprendizaje` del que colgarse -- `obtener_resultado_aprendizaje()` es función nueva del módulo abierto por [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md).
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`abrirResultadoAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/README.md).
- [`abrirPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionEvaluacion/README.md) -- precedente de lectura simple por identificador.
