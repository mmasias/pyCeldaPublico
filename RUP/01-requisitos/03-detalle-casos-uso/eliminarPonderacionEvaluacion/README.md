<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarPonderacionEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarPonderacionEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Eliminar un `PonderacionEvaluacion` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver modelo del dominio (`DirectorGrado --|> Profesor`).

**Sin `<<choice>>` bloqueante, a diferencia de la mayoría de `eliminarX()` del catálogo**: nada depende estructuralmente de una `PonderacionEvaluacion` (no es padre de ninguna otra entidad, a diferencia de `Materia`/`ResultadoAprendizaje`), así que no hay nada que bloquear -- confirmación simple, mismo patrón sin `<<choice>>` que los `desasignar`/`desasociar` de L6/L7. Que la suma deje de dar 100% o que la suma de un `SistemaEvaluacion` caiga fuera de rango tras el borrado no se avisa aquí: ambas validaciones ya están cubiertas en otro punto del flujo -- la primera en [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) (ya cerrado), la segunda en el próximo `crearPonderacionEvaluacion()`/`editarPonderacionEvaluacion()` que se intente sobre ese mismo `SistemaEvaluacion`.

Solicitada desde el listado ([`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md)), no desde el detalle -- mismo patrón que [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md).

**Datos en memoria**: la eliminación no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : eliminarPonderacionEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PonderacionEvaluacion`
- Modelo del dominio -- `Guia *-d- PonderacionEvaluacion`, sin entidad que dependa de ella
