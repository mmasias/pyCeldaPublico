<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`Profesor`; `DirectorPrograma` como corrección excepcional de la `Guia`|
|**Objetivo**|Crear una `ReferenciaBibliografica` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**`DirectorPrograma` como corrección excepcional.** Además del `Profesor`, el `DirectorPrograma` del `Programa` de la `Guia` puede ejecutar este caso de uso sobre ella, como corrección directa. Regla de transición: `Aprobada -> Borrador` (`revocarAprobacion()`) y `EnRevision -> Rechazada` (`rechazar()`); `Borrador` y `Rechazada` se mantienen. Cada transición real registra un `HistorialCambio` con `campo="estado"`, autor el Director y comentario "corrección directa del Director". Un `DirectorPrograma` que no dirige el `Programa` de la `Guia` recibe `404`. El Director no gana `enviarGuiaARevision()`: el envío a revisión sigue siendo del `Profesor`. Si el mismo email resuelve a `Profesor` que imparte la asignatura y a `DirectorPrograma`, gana la rama `Profesor` (sin transición de estado). Sin validación de negocio que pueda impedirla, la transición se aplica siempre que el Director escribe.

**CRUD estándar sin `<<choice>>`**, a diferencia de [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md): `ReferenciaBibliografica` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio -- confirmado sin hueco de diseño en la discussion [#38](https://github.com/mmasias/pyCelda/discussions/38), se construyó sin esperar a su cierre. `tipo` es el enum cerrado de 4 valores (`Basica`, `Complementaria`, `WebsReferencia`, `OtrasFuentes` en el modelo de dominio; mostrados en el wireframe con su forma legible real -- "Básica", "Complementaria", "Webs de referencia", "Otras fuentes de consulta", corregido tras detectar que el dropdown mostraba el literal del enum en vez del texto real -- ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)), `referencia` texto libre -- mismo tratamiento de `tipo` que [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md).

`ReferenciaBibliografica{tipo, referencia}` es igual de minimalista que `PonderacionEvaluacion`, así que pide ambos campos de una vez -- mismo criterio que cerró [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) en la revisión de L3.

**Datos en memoria**: la referencia creada no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md). La otra vía de alta de `ReferenciaBibliografica` es [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)), que crea las filas por copia desde una guía hermana -- real e inmediata (no en memoria) y replicando el flag `vinculada` del origen, a diferencia del alta manual que siempre nace `vinculada=False`.

**Tope de longitud de la `referencia`** (issue [#669](https://github.com/mmasias/pyCelda/issues/669)): el texto de la `ReferenciaBibliografica` admite como máximo 500 caracteres (`LIMITE_REFERENCIA_BIBLIOGRAFICA`). Si se supera, el backend responde `422` con `La referencia bibliográfica supera el límite de 500 caracteres`. Barrera de entrada, no precondición del dominio: sin `<<choice>>` en la especificación. El campo del cliente lleva `maxlength` 500, sin contador visible.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : crearReferenciaBibliografica()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`, `ReferenciaBibliografica{tipo, referencia}`
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- confirma que `ReferenciaBibliografica` no tiene hueco de diseño
