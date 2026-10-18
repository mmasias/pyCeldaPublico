<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Eliminar una `ActividadFormativa` del catálogo de un `Programa`, siempre que ninguna `Materia` ni `AsignaturaPrograma` del programa tenga horas repartidas en ella|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente (issue [#772](https://github.com/mmasias/pyCelda/issues/772)). Una `ActividadFormativa` está **en uso** cuando alguna `Materia` del programa, o alguna de sus `AsignaturaPrograma`, tiene **horas > 0** en ella. Las filas a 0 son autopoblado (toda `Materia`/`AsignaturaPrograma` tiene una por cada actividad del catálogo de su `Programa`) y no cuentan como uso: si contaran, ninguna actividad sería nunca eliminable. Al eliminar, esas filas a 0 se retiran con ella.

A diferencia de [`eliminarCompetencia()`](../eliminarCompetencia/README.md), el `<<choice>>` va **después** de la confirmación: la pantalla de confirmación presenta código y nombre, y el bloqueo aparece al confirmar, con el mensaje del sistema que nombra las `Materia` afectadas (también cuando las horas están en una de sus `AsignaturaPrograma`). No hay una consulta previa de asignaciones que mostrar: la ficha no tiene distribución (ver [`abrirActividadFormativa()`](../abrirActividadFormativa/README.md)). Desbloqueo: poner a 0 las horas en esas materias y en sus asignaturas.

**Histórico**: hasta #772 el catálogo era de la `Universidad` y el caso de uso era solo de `Admin`; la regla de bloqueo (horas > 0) es la misma desde #655.

Códigos y nombres de los wireframes ilustrativos.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : eliminarActividadFormativa()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : eliminarActividadFormativa()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas, porcentajePresencialidad}`, `ActividadFormativaAsignaturaPrograma{horas}` (origen de la regla de bloqueo); [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), entrada `ActividadFormativa`
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
