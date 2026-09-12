<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPonderacionesEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Consultar el listado de `PonderacionEvaluacion` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) (`DirectorGrado --|> Profesor`).

**Dos entradas, un solo retorno**, mismo patrón que [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md): desde `GUIA_ABIERTO` (primera apertura) y desde `PONDERACION_EVALUACION_ABIERTO` (vuelta desde el detalle, reutilizando el mismo verbo plural en vez de inventar un `volverAPonderaciones()`) -- ambas presentan exactamente lo mismo, el listado completo. La salida hacia `GUIA_ABIERTO` reutiliza a su vez [`abrirGuia()`](../abrirGuia/README.md), ya cerrado en L7.

Primer listado del catálogo con columna de `SistemaEvaluacion` -- necesaria porque una `PonderacionEvaluacion` no tiene sentido sin saber a qué sistema de evaluación pertenece (ver [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md)). Datos reales de `GII__IYA003` ya usados en [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md)/[`abrirGuia()`](../abrirGuia/README.md): las tres primeras (Examen Parcial 25%, Actividades y ejercicios 20%, Interés y participación 5%) pertenecen a `Evaluación continua`, la cuarta (Examen Teórico-Práctico 50%) a `Evaluación final` -- reparto reconstruido a partir de los rangos reales de la Materia (ver discussion [#38](https://github.com/mmasias/pyCelda/discussions/38)), no aportado como tal en el seed.

**Medidor de completitud** (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), ajuste B). El listado hace visibles, mientras el `Profesor` edita, las dos condiciones de ponderación que hoy solo se descubren al recibir el rechazo de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) (`Guia.puede_enviarse_a_revision()`): "Total asignado: X% / 100%" bajo el listado (resaltado si no suma 100), y una columna "Asignado" en la tabla de sistemas de evaluación de la materia, con cada subtotal contra su `[ponderaciónMínima, ponderaciónMáxima]` (resaltado si cae fuera). Se cuentan todas las filas visibles -- vinculadas y pendientes de vincular, las que se enviarán en `ids_ponderaciones_final` -- descontando las excluidas de la lista de trabajo local. Es presentación: no cambia el flujo ni la especificación, solo el `wireframe`. El mismo medidor se replica en la sección "Evaluación" de [`abrirGuia()`](../abrirGuia/README.md). El equivalente para la planificación docente ("N / M sesiones") se aborda en el ajuste A de la misma discussion.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : abrirPonderacionesEvaluacion()`, `PONDERACION_EVALUACION_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : abrirPonderacionesEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PonderacionEvaluacion`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-d- PonderacionEvaluacion`, `PonderacionEvaluacion -> SistemaEvaluacion`
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre de la validación de rango, origen del reparto por `SistemaEvaluacion` mostrado aquí
