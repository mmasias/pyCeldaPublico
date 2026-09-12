<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
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
|**Actor**|`DirectorGrado`|
|**Objetivo**|Editar las `horas` del reparto de las 10 `ActividadFormativa` de una `Materia` (`ActividadFormativaMateria`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

El `DirectorGrado` teclea las horas de cada una de las **10 actividades formativas** de la `Materia` en una rejilla y guarda de una sola vez -- la unidad de trabajo es el reparto de la materia, no una actividad suelta (por eso el caso de uso va en plural y no hay `asociar`/`desasociar`: las 10 filas están siempre presentes, autopobladas a 0 al crear la `Materia`). `codigo`/`nombre` de cada `ActividadFormativa` se muestran de solo lectura -- son catálogo institucional seed-estático de `Universidad`, no se editan desde ningún caso de uso.

`horas` admite decimales. El único fallo posible es un valor negativo (`<<choice>>` tras la entrada de datos, mismo mecanismo que `crearPonderacionEvaluacion()`): rojo rechaza el guardado completo y vuelve a `MATERIA_ABIERTO` sin escribir nada; verde persiste las 10 filas.

**La regla `AfM = Σ AfAdM`** (horas de la materia = suma de las horas de sus `AsignaturaGrado`) **NO se valida aquí** -- es validación blanda, vive en [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) (medidor que marca discrepancias sin bloquear), mismo espíritu que `Guia.bloqueo_ponderaciones()`. El reparto se construye de forma incremental sin que el sistema impida guardar un estado intermedio que aún no cuadra.

Retoca [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md): la pantalla de detalle de `Materia` gana la sección "Actividades formativas" con la rejilla y el botón de entrada a este caso de uso, sin tocar la especificación de `abrirMateria()` -- mismo criterio que los retoques de L2/L4/L5.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarActividadesFormativasMateria()` (verde y rojo, ambas al mismo estado -- ver regla de la rama de fallo en el [README de Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md))
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas}`, `(Materia, ActividadFormativa) .. ActividadFormativaMateria`; README: "invariante de autopoblado... la reparte el `DirectorGrado` en dos niveles estructurales"
- [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) -- el mismo reparto en el nivel inferior de la cascada, con `porcentajePresencialidad` además de `horas`
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas (gap 3 del backlog de la [#217](https://github.com/mmasias/pyCelda/discussions/217))
