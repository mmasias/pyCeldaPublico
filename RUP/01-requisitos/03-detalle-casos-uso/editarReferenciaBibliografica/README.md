<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`; `DirectorPrograma` como corrección excepcional de la `Guia`|
|**Objetivo**|Editar una `ReferenciaBibliografica` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**`DirectorPrograma` como corrección excepcional.** Además del `Profesor`, el `DirectorPrograma` del `Programa` de la `Guia` puede ejecutar este caso de uso sobre ella, como corrección directa. Regla de transición: `Aprobada -> Borrador` (`revocarAprobacion()`) y `EnRevision -> Rechazada` (`rechazar()`); `Borrador` y `Rechazada` se mantienen. Cada transición real registra un `HistorialCambio` con `campo="estado"`, autor el Director y comentario "corrección directa del Director". Un `DirectorPrograma` que no dirige el `Programa` de la `Guia` recibe `404`. El Director no gana `enviarGuiaARevision()`: el envío a revisión sigue siendo del `Profesor`. Si el mismo email resuelve a `Profesor` que imparte la asignatura y a `DirectorPrograma`, gana la rama `Profesor` (sin transición de estado). Sin validación de negocio que pueda impedirla, la transición se aplica siempre que el Director escribe.

Sin `<<choice>>`, mismo criterio que [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- ninguna validación cruzada que aplicar. `tipo` es editable igual que `referencia`, mismo criterio de "todo editable" que [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md).

**Datos en memoria**: los cambios no se persisten hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

**Tope de longitud de la `referencia`** (issue [#669](https://github.com/mmasias/pyCelda/issues/669)): el texto de la `ReferenciaBibliografica` admite como máximo 500 caracteres (`LIMITE_REFERENCIA_BIBLIOGRAFICA`). Si se supera, el backend responde `422` con `La referencia bibliográfica supera el límite de 500 caracteres`. Barrera de entrada, no precondición del dominio: sin `<<choice>>` en la especificación. El campo del cliente lleva `maxlength` 500, sin contador visible.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIA_BIBLIOGRAFICA_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : editarReferenciaBibliografica()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ReferenciaBibliografica{tipo, referencia}`
