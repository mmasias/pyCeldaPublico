<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirPonderacionEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirPonderacionEvaluacion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirPonderacionEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirPonderacionEvaluacion()`](/RUP/02-analisis/casos-uso/abrirPonderacionEvaluacion/README.md): lectura de una fila concreta, **sin endpoint nuevo** -- reutiliza `GET /api/v1/ponderaciones-evaluacion/{ponderacion_id}`, el mismo que ya invoca [`editarPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) para cargar el formulario. Primer caso de esta rebanada de 12 sin ningún endpoint propio.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirPonderacionEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirPonderacionEvaluacionView` (React) -- pide `GET /api/v1/ponderaciones-evaluacion/{ponderacion_id}`, sin formulario editable.
- **API**: `routers/ponderacion_evaluacion.py::obtener_ponderacion_evaluacion(ponderacion_id)` -- función ya existente, reutilizada tal cual (mismo endpoint que la primera mitad de `editarPonderacionEvaluacion()`).
- **Modelo**: ninguno con lógica propia invocada -- solo se serializa lo que devuelve el repositorio.
- **Repositorio**: `PonderacionEvaluacionRepository.obtener(ponderacion_id)`.

## Decisiones de diseño

- **Cero endpoints nuevos**: a diferencia del resto de la rebanada, este caso de uso no añade ninguna función a `routers/`. El diagrama de clases de Diseño no gana ninguna entrada nueva por este CU.
- **Sin capa Service**: no aplica de forma directa (no hay lógica que orquestar), pero se mantiene por consistencia documental.
- **Diferencia con `editarPonderacionEvaluacion()`**: la Vista de este caso no ofrece el selector de `SistemaEvaluacion` (`GET /api/v1/materias/{materia_id}/sistemas-evaluacion`) porque no hay formulario que rellenar, solo presentación.

## Referencias

- [`abrirPonderacionEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/abrirPonderacionEvaluacion/README.md) -- diagrama de colaboración origen, ya señalaba la reutilización de `cargarPonderacionEvaluacion(ponderacionId)`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/README.md).
- [`editarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- mismo endpoint `GET /api/v1/ponderaciones-evaluacion/{ponderacion_id}`, reutilizado aquí.
