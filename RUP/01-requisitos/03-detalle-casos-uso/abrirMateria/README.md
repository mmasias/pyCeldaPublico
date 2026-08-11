<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el detalle de una `Materia` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorGrado` (`DirectorGrado --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml).

Retocado el wireframe al construir L4 (mismo criterio que `abrirProfesor()` en L2, sin tocar la especificación): `MATERIA_ABIERTO` es el destino de los cinco self-loops de asociación (`asociarMetodologiaDocenteAMateria()`, `desasociarMetodologiaDocenteMateria()`, `editarAsociacionMetodologiaDocenteMateria()`, `asociarResultadoAprendizajeAMateria()`, `desasociarResultadoAprendizajeAMateria()`), así que el detalle de la Materia necesita mostrar ambas listas para que esos botones tengan sentido. No se añade botón hacia `SistemasEvaluacion` -- a diferencia de las asociaciones (self-loop sobre el propio `MATERIA_ABIERTO`), `abrirSistemasEvaluacion()` lleva a un estado hijo propio (`SISTEMAS_EVALUACION_ABIERTO`), mismo criterio por el que `abrirGrado()` tampoco muestra botones hacia `Materias`/`ResultadosAprendizaje`/`AsignaturasGrado`.

**Retocado de nuevo al construir L5**: `MATERIA_ABIERTO` es también la segunda entrada de [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) (ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `MATERIA_ABIERTO --> ASIGNATURA_GRADO_ABIERTO`), a diferencia de `SistemasEvaluacion` esta transición no lleva a un listado propio sino directo al detalle de una `AsignaturaGrado` concreta -- sin una mini-tabla aquí no habría forma de elegir cuál abrir. Solo `[Abrir]`, sin `[Eliminar]`/`+ Crear`: esas acciones son self-loops de `GRADO_ABIERTO` (ver retoque de [`abrirGrado()`](../abrirGrado/README.md)), no de `MATERIA_ABIERTO`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Materia`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- Modelo del dominio -- `Materia{nombre}`, `Grado *-- Materia`; Materia real de referencia (mezcla asignaturas Básicas y Obligatorias)
