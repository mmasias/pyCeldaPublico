<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar los datos de un `Grado` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado` (`DirectorGrado --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml).

**Retocado el wireframe al construir L5** (mismo criterio que el retoque de `abrirMateria()` en L4, sin tocar la especificación): `GRADO_ABIERTO` es el destino del atajo plano de `AsignaturaGrado` (`crearAsignaturaGrado()`/`eliminarAsignaturaGrado()` son self-loops sobre este mismo estado, `abrirAsignaturaGrado()` es la segunda entrada -- ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)), así que el detalle del Grado necesita mostrar la tabla de `AsignaturaGrado` (agrupada por `Materia`, columna propia en la tabla) para que esos botones tengan sentido. No se añaden botones hacia `Materias`/`ResultadosAprendizaje`/`AsignaturasGrado` (plural, propio de `DirectorGrado`): esas transiciones llevan a un estado hijo propio, mismo criterio ya documentado en [`abrirMateria()`](../abrirMateria/README.md) para `SistemasEvaluacion`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Grado`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- Modelo del dominio -- `Grado { codigo, estado }`
