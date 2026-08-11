<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirGrados()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `Grado`s de una `Facultad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado` (`DirectorGrado --|> Profesor`) como punto de entrada tras iniciar sesión, con una diferencia de contexto: el listado que ve `Admin` es el de una `Facultad` concreta ya abierta, mientras que `DirectorGrado` ve directamente el listado de los Grados que dirige -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml). Una sola especificación, no duplicada.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTAD_ABIERTO --> GRADOS_ABIERTO : abrirGrados()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `SESION_CERRADA --> GRADOS_ABIERTO : iniciarSesion()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Grado`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- Modelo del dominio -- `Facultad *-d- Grado` (composición: origen de la jerarquía de navegación)
