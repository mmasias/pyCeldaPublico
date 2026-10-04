<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearFacultad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearFacultad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearFacultad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta una `Facultad` en una `Universidad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

## Notas de diseño y trazabilidad

- El botón "Crear Facultad" está en la pantalla `Universidad` (datos de la Universidad más la lista de sus Facultades), no en un listado `FACULTADES_ABIERTO` propio, aunque el diagrama de contexto sitúe la transición en `FACULTADES_ABIERTO` (issue [#625](https://github.com/mmasias/pyCelda/issues/625), activado en [#626](https://github.com/mmasias/pyCelda/issues/626)).
- La salida `<<include>> editarFacultad()` no se materializa: tras crear se navega al detalle de la Facultad, donde "Editar" sigue deshabilitado.
- El formulario de la pantalla incluye también un botón "Cancelar" que vuelve a la `Universidad`. No se dibuja en el wireframe ni se narra en la especificación para mantener la misma convención que [`crearPrograma()`](../crearPrograma/README.md) y [`crearMateria()`](../crearMateria/README.md), cuyas pantallas lo tienen igualmente sin reflejarlo.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTADES_ABIERTO --> FACULTAD_ABIERTO : crearFacultad()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Facultad`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Facultad`, sin más atributos que `nombre` (demasiado simple para diagramarlo, ver README de esa fase)
