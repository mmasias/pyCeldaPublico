<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > quitarDirectorGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (único DirectorGrado del Grado)|Confirmación (queda otro DirectorGrado)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Quitar el rol `DirectorGrado` a un `Profesor` sobre un `Grado` concreto, siempre que quede al menos otro director|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Mismo patrón `<<choice>>` bloqueante que `eliminarFacultad()`/`eliminarProfesor()`**, aplicado a quitar un rol en vez de a borrar una entidad: un `Grado` no puede quedarse sin ningún `DirectorGrado`, así que el `<<choice>>` valida al inicio, antes de presentar la pantalla de confirmación -- si el `Profesor` es el único director de ese `Grado`, el sistema bloquea sin llegar a preguntar "¿seguro?". Decisión cerrada en la discussion [#18](https://github.com/mmasias/pyCelda/discussions/18).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : quitarDirectorGrado()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor`
- Modelo del dominio -- `Grado o- DirectorGrado` (agregación, muchos a muchos)
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del `<<choice>>` bloqueante
- [`definirDirectorGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/README.md) -- caso de uso complementario (alta del rol)
