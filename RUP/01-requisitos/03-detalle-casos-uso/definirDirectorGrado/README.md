<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > definirDirectorGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Nombrar a un `Profesor` ya abierto como `DirectorGrado` de un `Grado` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`DirectorGrado` no es una entidad propia sino un rol sobre un `Profesor` ya abierto (`PROFESOR_ABIERTO`) -- el flujo empieza desde el Profesor, con selector de Grado, no al revés desde el Grado (decisión cerrada en la discussion [#18](https://github.com/mmasias/pyCelda/discussions/18), flujo inverso descartado como extensión trivial futura). Cardinalidad `Grado`-`DirectorGrado` muchos a muchos: **asignación libre, sin `<<choice>>`** -- un Grado admite varios directores simultáneos (cubre la figura del coordinador) y un Profesor puede dirigir varios Grados a la vez, así que no hay ninguna exclusión que validar. El selector solo excluye los Grados que el Profesor ya dirige, por no tener sentido repetir la asignación.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : definirDirectorGrado()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor`
- Modelo del dominio -- `Grado o- DirectorGrado` (agregación, muchos a muchos)
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre de flujo, cardinalidad y ausencia de `<<choice>>`
- [`quitarDirectorGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/README.md) -- caso de uso complementario (baja del rol)
