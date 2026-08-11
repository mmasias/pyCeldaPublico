<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el detalle de un `Profesor` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

`PROFESOR_ABIERTO` también aloja `definirDirectorGrado()`/`quitarDirectorGrado()` (self-loop, ver diagrama de contexto) -- casos de uso de una capa posterior (L2), sin especificación propia todavía. Este wireframe no anticipa esos botones; se añadirán a esta misma pantalla cuando se detallen.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESOR_ABIERTO : abrirProfesor()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor`
- Datos reales: `docs/scripts/seed/profesores.json` (repo privado)
