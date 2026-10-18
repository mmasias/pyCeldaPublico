<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarModulo/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarModulo/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarModulo()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarModulo/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarModulo/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (con materias)|Confirmación (sin materias)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Eliminar un `Modulo` que no tenga materias|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado si alguna `Materia` está en el módulo (#762, decisión 4); el bloqueo nombra las materias y el servidor lo vuelve a comprobar (409). Para vaciarlo, se cambia el módulo de esas materias en [`editarMateria()`](../editarMateria/README.md). Datos de los wireframes ilustrativos: los módulos reales de cada programa se importarán de las memorias una vez implementado (#762, decisión 8).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MODULOS_ABIERTO --> MODULOS_ABIERTO : eliminarModulo()`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Modulo o-- Materia`
- Issue [#762](https://github.com/mmasias/pyCelda/issues/762)
