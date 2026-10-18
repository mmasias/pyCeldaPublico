<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/abrirSistemaEvaluacion/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Recupera un `SistemaEvaluacion` por identificador para presentarlo en detalle -- mismo patrón de lectura simple que `abrirResultadoAprendizaje()`. Es también el destino del alta de `crearSistemaEvaluacion()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `SistemaEvaluacion` (React, ruta `/admin/sistemas-evaluacion/:id`) -- pide `GET /api/v1/sistemas-evaluacion/{sistema_evaluacion_id}`; muestra `codigo` (`--` si es nulo), `tipo`, `descripcion`, `ponderacion_minima`, `ponderacion_maxima`; botones `[Editar]` y `[Volver al listado]`.
- **API**: `routers/sistema_evaluacion.py::obtener_sistema_evaluacion(sistema_evaluacion_id)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- `SistemaEvaluacion` solo porta los datos presentados.
- **Repositorio**: `SistemaEvaluacionRepository.obtener(sistema_evaluacion_id)` -- `SELECT` por identificador, método ya existente reutilizado.

## Decisiones de diseño

- **Endpoint propio, sin colisión con el picker de `Profesor`**: a diferencia del listado ([`abrirSistemasEvaluacion()`](../abrirSistemasEvaluacion/README.md), que necesita namespace `/admin/`), este path estaba libre -- `GET /api/v1/sistemas-evaluacion/{id}` con `require_admin` directo.
- **`materia_id` en la respuesta**: la Vista necesita saber a qué `Materia` volver (`[Volver al listado]`) sin mantener estado de navegación -- `SistemaEvaluacionResponse` lo expone; ya vive en el modelo.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.
- **Sin capa Service**: Router delgado -> Repository.

**`codigo` (issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: columna `sistemas_evaluacion.codigo VARCHAR(20) NULL` (esquema versión 4), el código de la memoria (p. ej. `E1`). En `_DatosSistemaEvaluacion` (base de `SistemaEvaluacionCreate`/`Update`) es `str | None`; un validador recorta espacios, aplica `validar_longitud(valor, 20, "El código")` y convierte el vacío en `None`. Sin unicidad: no hay restricción por `Materia` ni por `Programa`. `SistemaEvaluacionResponse` lo expone como `codigo: str | None`. `descripcion` no cambia de tipo; cambia su significado (denominación literal de la memoria).

## Referencias

- [`abrirSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/abrirSistemaEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/README.md).
- [`abrirResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/abrirResultadoAprendizaje/README.md) -- precedente de lectura simple por identificador bajo un padre.
