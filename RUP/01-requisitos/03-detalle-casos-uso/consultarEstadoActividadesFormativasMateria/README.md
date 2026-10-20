<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Sin optatividad|Con optatividad|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframe-optatividad.svg)|
|<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|<sup>mismo fichero, segundo bloque `@startsalt`</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Consultar el estado de las actividades formativas de una `Materia`: por cada `ActividadFormativa`, las `horas` de la materia frente a la suma de las de sus `AsignaturaPrograma` (regla `AfM = Σ AfAdM`), con las discrepancias marcadas; y el total de horas de la materia frente a 25 h por ECTS|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Medidor de la regla **`AfM = Σ AfAdM`** (actividades formativas de la materia = suma de las de sus asignaturas). Se compone desde [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md) -- self-loop de `MATERIA_ABIERTO`, mismo patrón que `previsualizarGuia()` sobre `GUIA_ABIERTO` (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)): un CU propio, de solo lectura, que otra pantalla incrusta.

**Validación blanda, no un gate**: presenta las actividades formativas del catálogo del `Programa` (una fila por actividad) con `horas` de la materia (`ActividadFormativaMateria`), la suma de `horas` de sus `AsignaturaPrograma` (`ActividadFormativaAsignaturaPrograma`) y la diferencia; marca las que no cuadran. **No bloquea ningún guardado** -- ni el de [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) ni el de [`editarActividadesFormativasAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md). El `DirectorPrograma` construye el reparto de forma incremental y usa el medidor para saber qué falta cuadrar. Mismo espíritu que `Guia.bloqueo_ponderaciones()` (que sí bloquea el envío a revisión, pero es un medidor de mensaje, no una excepción) -- aquí ni siquiera hay envío que bloquear, es puramente informativo.

Sin `<<choice>>` -- no hay rama de fallo, solo la presentación del estado. Verbo `consultar` ya existente en el catálogo (`consultarEstadoGuias()` es el precedente exacto: un `read` que agrega estado y lo presenta), forma relajada `consultarEstado...()`.

**Comprobación por ECTS** (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): con `Materia.ects` (dato aprobado de la memoria, que escribe la importación desde el RUCT) el medidor añade una segunda comprobación, también blanda: la suma de `horas` de la materia frente a 25 h por ECTS (`ects × 25`), con las horas esperadas, las de la materia, si cuadra y la diferencia. Sin `ects` (materia no importada del RUCT) no hay con qué comparar y la comprobación no se presenta. **No reparte nada**: el reparto proporcional automático entre las `AsignaturaPrograma` se descartó en #768, y la comprobación se hace contra la `Materia`, no contra la suma de ECTS de sus asignaturas (por optatividad no siempre coinciden). Hasta #772 no se comparaba nada con ECTS (decisión de la discussion [#227](https://github.com/mmasias/pyCelda/discussions/227), cuando `Materia` no tenía `ects`).

**Materia con optatividad** (issue [#786](https://github.com/mmasias/pyCelda/issues/786)): una `Materia` tiene optatividad cuando sus horas suman 25 h por ECTS y sus `AsignaturaPrograma` no suman sus ECTS -- idiomas alternativos, optativas, o asignaturas de la memoria que el sistema tiene en otra materia. Cada `AsignaturaPrograma` lleva entonces 25 h por ECTS (la comprobación de [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md)) y la suma de sus horas supera, o no alcanza, la de la materia por construcción: la regla `AfM = Σ AfAdM` no se cumple por diseño. En ese caso el medidor no compara por actividad ni marca discrepancias; en su lugar presenta los ECTS que suman sus asignaturas frente a los de la materia y explica que la suma de sus horas no se compara (segundo wireframe). La comprobación por ECTS de la materia se presenta igual. Sin `ects` en la `Materia` no hay optatividad que detectar y la regla se compara como siempre.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: `Admin` ve también el medidor en su ficha de `Materia`, con la misma tabla y el mismo carácter informativo. Self-loop de `MATERIA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml).


## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : consultarEstadoActividadesFormativasMateria()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas, porcentajePresencialidad}`, `ActividadFormativaAsignaturaPrograma{horas}`, `Materia.ects`; README: "Regla `AfM = Σ AfAdM`: validación blanda a nivel de `Materia`" y la segunda comprobación por ECTS
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) / [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- los dos repartos que este medidor contrasta
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo `consultarEstado...()`
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas y decisión de la validación blanda
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772) -- `Materia.ects` y la comprobación de horas por ECTS
- Issue [#786](https://github.com/mmasias/pyCelda/issues/786) -- materia con optatividad: la regla `AfM = Σ AfAdM` no se compara
