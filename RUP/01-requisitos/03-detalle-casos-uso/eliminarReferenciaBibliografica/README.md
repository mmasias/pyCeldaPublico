<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarReferenciaBibliografica/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarReferenciaBibliografica/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarReferenciaBibliografica/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarReferenciaBibliografica/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`; `DirectorPrograma` como corrección excepcional de la `Guia`|
|**Objetivo**|Eliminar una `ReferenciaBibliografica` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**`DirectorPrograma` como corrección excepcional.** Este caso de uso no tiene endpoint propio: la eliminación queda excluida de la lista de trabajo y se persiste al guardar con [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md), que desvincula (borra) la fila. Como `guardarBorradorGuia()` admite al `DirectorPrograma` sobre las `Guia` de los `Programa` que dirige, el Director también puede eliminar desde las pantallas de gestión, y es ese guardado el que dispara la transición. Regla de transición: `Aprobada -> Borrador` (`revocarAprobacion()`) y `EnRevision -> Rechazada` (`rechazar()`); `Borrador` y `Rechazada` se mantienen. Cada transición real registra un `HistorialCambio` con `campo="estado"`, autor el Director y comentario "corrección directa del Director". Un `DirectorPrograma` que no dirige el `Programa` de la `Guia` recibe `404`. El Director no gana `enviarGuiaARevision()`: el envío a revisión sigue siendo del `Profesor`. Si el mismo email resuelve a `Profesor` que imparte la asignatura y a `DirectorPrograma`, gana la rama `Profesor` (sin transición de estado).

**Sin `<<choice>>` bloqueante**, mismo criterio que [`eliminarPonderacionEvaluacion()`](../eliminarPonderacionEvaluacion/README.md): nada depende estructuralmente de una `ReferenciaBibliografica`. Solicitada desde el listado ([`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md)), no desde el detalle.

**Datos en memoria**: la eliminación no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : eliminarReferenciaBibliografica()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`, sin entidad que dependa de ella
