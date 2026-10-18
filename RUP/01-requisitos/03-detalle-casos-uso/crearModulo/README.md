<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearModulo/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearModulo/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearModulo()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearModulo/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearModulo/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearModulo/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearModulo/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta un `Modulo` en un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`codigo` y `nombre` obligatorios, `descripcion` opcional. `<<choice>>` de código repetido dentro del `Programa`, mismo mecanismo que `crearCompetencia()`. Sin `<<include>>` de edición: no hay ficha del módulo, la salida es el listado actualizado. Asignar materias al módulo no es parte de este caso de uso: se hace en [`crearMateria()`](../crearMateria/README.md)/[`editarMateria()`](../editarMateria/README.md) (desplegable **Módulo**). Datos de los wireframes ilustrativos: los módulos reales de cada programa se importarán de las memorias una vez implementado (#762, decisión 8).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MODULOS_ABIERTO --> MODULOS_ABIERTO : crearModulo()`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Modulo{codigo, nombre, descripcion}`
- Issue [#762](https://github.com/mmasias/pyCelda/issues/762)
