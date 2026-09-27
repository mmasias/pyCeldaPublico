<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > eliminarPonderacionEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPonderacionEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarPonderacionEvaluacion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/eliminarPonderacionEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`eliminarPonderacionEvaluacion()`](/RUP/02-analisis/casos-uso/eliminarPonderacionEvaluacion/README.md): **sin endpoint de backend** -- decisión 2 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58). Confirmar/cancelar es una mutación de la lista de trabajo del cliente: el `Profesor` quita el ítem de un array en estado local de React, sin ninguna llamada a la API. Es, deliberadamente, el primer caso de la rebanada cuya secuencia de diseño no tiene ni Router ni Repository ni Base de Datos -- mismo motivo por el que Análisis ya lo cerró sin ninguna clase de Modelo en su diagrama de colaboración: no hay ninguna entidad de dominio ni persistencia involucrada en la operación. El efecto real solo se materializa después, cuando [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) reciba la lista completa (ya sin este `id`) y desvincule la fila real por ausencia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarPonderacionEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarPonderacionEvaluacionView` (React) -- presenta la confirmación y, en la rama verde, quita el `id` del array de trabajo en estado local (`useState`/reducer del listado), sin red.
- **API**: ninguna -- sin ruta HTTP para este caso de uso.
- **Modelo**: ninguno -- ninguna fila de `PonderacionEvaluacion` se lee, borra ni edita.
- **Repositorio**: ninguno.

## Decisiones de diseño

- **Sin endpoint de backend, por diseño**: 7 de los 9 casos de la rebanada tienen ruta real; este y [`eliminarReferenciaBibliografica()`](/RUP/03-diseño/casos-uso/eliminarReferenciaBibliografica/README.md) son los dos que no la tienen -- decisión 2 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58). No es una omisión de este README: es la implementación mínima real de la rebanada.
- **La eliminación es reversible hasta que se guarda el borrador**: si el `Profesor` cierra la pestaña sin guardar, el ítem sigue vinculado en la base de datos -- la lista de trabajo en memoria del cliente no tiene efecto hasta que `guardarBorradorGuia()` la reciba completa.
- **Ambas ramas (confirmar/cancelar) terminan en la misma pantalla** -- self-loop, sin navegación de salida distinta.

## Referencias

- [`eliminarPonderacionEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/eliminarPonderacionEvaluacion/README.md) -- diagrama de colaboración origen, ya sin ninguna clase de Modelo.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPonderacionEvaluacion/README.md).
- [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- quien recibe la lista de trabajo ya sin este ítem y desvincula la fila real por ausencia.
- [`eliminarReferenciaBibliografica()`](/RUP/03-diseño/casos-uso/eliminarReferenciaBibliografica/README.md) -- mismo patrón, sobre `ReferenciaBibliografica`.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- decisión 2, sin endpoint de backend para ambos `eliminar*()`.
