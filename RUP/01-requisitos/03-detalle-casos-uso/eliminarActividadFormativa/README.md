<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`Admin`|
|**Objetivo**|Eliminar una `ActividadFormativa` del catálogo institucional, siempre que ninguna `Materia`/`AsignaturaPrograma` tenga horas repartidas en ella|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que `eliminarMetodologiaDocente()`. Una `ActividadFormativa` está "en uso" cuando alguna `Materia` o `AsignaturaPrograma` de su `Universidad` tiene **horas > 0** repartidas en ella: las filas a 0 son autopoblado (toda `Materia`/`AsignaturaPrograma` tiene una por cada `ActividadFormativa` de su `Universidad`, issue #655) y no cuentan como uso -- si contaran, ninguna actividad sería nunca eliminable. Al eliminar, esas filas a 0 se retiran con ella. La pantalla bloqueada muestra el `detail` del 409 (nombres de las `Materia` afectadas). Elección de AF1/AF7 para bloqueada/confirmación es ilustrativa.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : eliminarActividadFormativa()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `ActividadFormativa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- ActividadFormativa` vía `ActividadFormativaMateria { horas }` (origen de la regla de bloqueo)
