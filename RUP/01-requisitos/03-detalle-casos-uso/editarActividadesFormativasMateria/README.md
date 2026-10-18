<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Editar las `horas` y el `porcentajePresencialidad` de las actividades formativas de una `Materia` (`ActividadFormativaMateria`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

El `DirectorPrograma` teclea, en una rejilla, las horas y el porcentaje de presencialidad de cada actividad formativa de la `Materia` y guarda de una sola vez -- la unidad de trabajo es el reparto de la materia, no una actividad suelta (por eso el caso de uso va en plural y no hay `asociar`/`desasociar`). La rejilla tiene **una fila por cada `ActividadFormativa` del catálogo del `Programa`** de la materia, siempre presente: se crea a 0 al dar de alta la `Materia` o la actividad (invariante de autopoblado, issue [#772](https://github.com/mmasias/pyCelda/issues/772)). `codigo`/`nombre` de cada actividad se muestran de solo lectura: se editan en el catálogo del programa ([`editarActividadFormativa()`](../editarActividadFormativa/README.md)), no desde aquí.

**Presencialidad en la `Materia`** (#772): la memoria fija el porcentaje de presencialidad por `Materia` y actividad formativa, así que se edita aquí, no en cada `AsignaturaPrograma`. Las asignaturas de la materia solo reparten horas y presentan esta presencialidad de solo lectura ([`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md)). Hasta #772 la presencialidad vivía en la `AsignaturaPrograma` y esta rejilla solo tenía horas.

`horas` y presencialidad admiten decimales. El único fallo posible es un valor fuera de rango -- horas negativas o presencialidad fuera de 0-100 (`<<choice>>` tras la entrada de datos, mismo mecanismo que `crearPonderacionEvaluacion()`): rojo rechaza el guardado completo y vuelve a `MATERIA_ABIERTO` sin escribir nada; verde persiste todas las filas.

**Total frente a ECTS**: si la `Materia` tiene `ects` (lo escribe la importación desde el RUCT, #772), la rejilla presenta el total de horas frente a 25 h por ECTS e indica si cuadra. Es informativo: no bloquea el guardado ni reparte nada. La misma comprobación aparece en la ficha de la materia ([`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md)).

**La regla `AfM = Σ AfAdM`** (horas de la materia = suma de las horas de sus `AsignaturaPrograma`) **NO se valida aquí** -- es validación blanda, vive en [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) (medidor que marca discrepancias sin bloquear), mismo espíritu que `Guia.bloqueo_ponderaciones()`. El reparto se construye de forma incremental sin que el sistema impida guardar un estado intermedio que aún no cuadra.

Retoca [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md): la pantalla de detalle de `Materia` gana la sección "Actividades formativas de la materia" (horas y presencialidad) con el botón de entrada a este caso de uso, sin tocar la especificación de `abrirMateria()` -- mismo criterio que los retoques de L2/L4/L5.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: `Admin` gana esta transición como vía de corrección, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `MATERIA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `Materia`. Motivo: tras la carga de horas desde las memorias ANECA (#754), Admin necesita poder completar o corregir las de los programas que la carga automática no cubre.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarActividadesFormativasMateria()` (verde y rojo, ambas al mismo estado -- ver regla de la rama de fallo en el [README de Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md))
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas, porcentajePresencialidad}`, `(Materia, ActividadFormativa) .. ActividadFormativaMateria`; README: "invariante de autopoblado... la reparte el `DirectorPrograma` en dos niveles estructurales"
- [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- el mismo reparto en el nivel inferior de la cascada, solo con `horas` (la presencialidad se hereda de la `Materia`)
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772) -- presencialidad en la `Materia`, catálogo del `Programa`, `Materia.ects`
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas (gap 3 del backlog de la [#217](https://github.com/mmasias/pyCelda/discussions/217))
