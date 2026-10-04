<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el detalle de una `Materia` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorPrograma` (`DirectorPrograma --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml).

Retocado el wireframe al construir L4 (mismo criterio que `abrirProfesor()` en L2, sin tocar la especificación): `MATERIA_ABIERTO` es el destino de los cinco self-loops de asociación (`asociarMetodologiaDocenteAMateria()`, `desasociarMetodologiaDocenteMateria()`, `editarAsociacionMetodologiaDocenteMateria()`, `asociarResultadoAprendizajeAMateria()`, `desasociarResultadoAprendizajeAMateria()`), así que el detalle de la Materia necesita mostrar ambas listas para que esos botones tengan sentido. No se añade botón hacia `SistemasEvaluacion` -- a diferencia de las asociaciones (self-loop sobre el propio `MATERIA_ABIERTO`), `abrirSistemasEvaluacion()` lleva a un estado hijo propio (`SISTEMAS_EVALUACION_ABIERTO`), mismo criterio por el que `abrirPrograma()` tampoco muestra botones hacia `Materias`/`ResultadosAprendizaje`/`AsignaturasPrograma`.

**Columna "Asignaturas"** ([discussion #585](https://github.com/mmasias/pyCelda/discussions/585), issue #586): la tabla de Resultados de aprendizaje gana el número de `AsignaturaPrograma` **de esta materia** que tienen ese RA asociado. Puramente informativo, sin bloquear nada ni filtrar por `caracter`.

**Retocado de nuevo al construir L5**: `MATERIA_ABIERTO` es también la segunda entrada de [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md) (ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `MATERIA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO`), a diferencia de `SistemasEvaluacion` esta transición no lleva a un listado propio sino directo al detalle de una `AsignaturaPrograma` concreta -- sin una mini-tabla aquí no habría forma de elegir cuál abrir. Solo `[Abrir]`, sin `[Eliminar]`/`+ Crear`: esas acciones son self-loops de `PROGRAMA_ABIERTO` (ver retoque de [`abrirPrograma()`](../abrirPrograma/README.md)), no de `MATERIA_ABIERTO`.

**Retocado el wireframe al construir el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227))**: `MATERIA_ABIERTO` gana la sección "Actividades formativas de la materia" -- una tabla con las 10 actividades formativas siempre presentes (`horas` de la materia y `Σ horas` de sus `AsignaturaPrograma`), con dos entradas nuevas: `[Editar reparto]` -> [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) (self-loop) y el medidor de la regla `AfM = Σ AfAdM` compuesto desde aquí ([`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md), self-loop informativo, no bloquea). Sin `+ Asociar`/`[Quitar]`: las 10 filas se autopueblan a 0 al crear la `Materia`, no se asocian ni se desasocian. No se toca la especificación de `abrirMateria()`.

**Retocado de nuevo al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496))**: la columna "Curso" de la tabla "Asignaturas de esta materia" combina ahora `curso` + `semestre_default` en un único valor con el curso en números romanos (`I-s1` en vez de `1`), mismo tratamiento y mismo issue ([#486](https://github.com/mmasias/pyCelda/issues/486)) que la tabla equivalente de [`abrirPrograma()`](../abrirPrograma/README.md). Sin cambio de dato ni de endpoint, sin tocar la especificación.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Materia`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- reutilización del caso de uso por `DirectorPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia{nombre}`, `Programa *-- Materia`; Materia real de referencia (mezcla asignaturas Básicas y Obligatorias)
