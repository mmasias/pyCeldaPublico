<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirModulos/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirModulos/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirModulos()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirModulos/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirModulos/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar los `Modulo` de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Pestaña **🧱 Módulos** del programa en la vista de Admin (`/admin/programas/:id/modulos`), issue [#762](https://github.com/mmasias/pyCelda/issues/762). El listado es también el punto de gestión: sin ficha propia del módulo (código, nombre y descripción caben en la fila), así que crear, editar y eliminar son autotransiciones de `MODULOS_ABIERTO`. **Nº de materias** cuenta las materias del programa asignadas a cada módulo.

El `DirectorPrograma` no tiene este caso de uso: ve el módulo de cada materia en [`abrirMaterias()`](../abrirMaterias/README.md) (agrupada por módulo) y en [`abrirMateria()`](../abrirMateria/README.md), sin gestionarlo (#762, decisión 6). Datos de los wireframes ilustrativos: los módulos reales de cada programa se importarán de las memorias una vez implementado (#762, decisión 8).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> MODULOS_ABIERTO : abrirModulos()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- package `Programa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Modulo`, `Modulo o-- Materia`
- Issue [#762](https://github.com/mmasias/pyCelda/issues/762)
