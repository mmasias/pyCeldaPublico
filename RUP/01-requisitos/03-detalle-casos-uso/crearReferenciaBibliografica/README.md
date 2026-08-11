<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Crear una `ReferenciaBibliografica` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver modelo del dominio (`DirectorGrado --|> Profesor`).

**CRUD estándar sin `<<choice>>`**, a diferencia de [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md): `ReferenciaBibliografica` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio -- confirmado sin hueco de diseño en la discussion [#38](https://github.com/mmasias/pyCelda/discussions/38), se construyó sin esperar a su cierre. `tipo` es el enum cerrado de 4 valores (`Basica`, `Complementaria`, `WebsReferencia`, `OtrasFuentes`), `referencia` texto libre -- mismo tratamiento de `tipo` que [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md).

`ReferenciaBibliografica{tipo, referencia}` es igual de minimalista que `PonderacionEvaluacion`, así que pide ambos campos de una vez -- mismo criterio que cerró [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) en la revisión de L3.

**Datos en memoria**: la referencia creada no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : crearReferenciaBibliografica()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- Modelo del dominio -- `Guia *-- ReferenciaBibliografica`, `ReferenciaBibliografica{tipo, referencia}`
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- confirma que `ReferenciaBibliografica` no tiene hueco de diseño
