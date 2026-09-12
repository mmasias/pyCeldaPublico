<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Consultar el estado de la regla `AfM = Σ AfAdM` de una `Materia`: por cada `ActividadFormativa`, las `horas` de la materia frente a la suma de las de sus `AsignaturaGrado`, con las discrepancias marcadas|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Medidor de la regla **`AfM = Σ AfAdM`** (actividades formativas de la materia = suma de las de sus asignaturas). Se compone desde [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md) -- self-loop de `MATERIA_ABIERTO`, mismo patrón que `previsualizarGuia()` sobre `GUIA_ABIERTO` (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)): un CU propio, de solo lectura, que otra pantalla incrusta.

**Validación blanda, no un gate**: presenta las 10 actividades formativas con `horas` de la materia (`ActividadFormativaMateria`), la suma de `horas` de sus `AsignaturaGrado` (`ActividadFormativaAsignaturaGrado`) y la diferencia; marca las que no cuadran. **No bloquea ningún guardado** -- ni el de [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) ni el de [`editarActividadesFormativasAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/README.md). El `DirectorGrado` construye el reparto de forma incremental y usa el medidor para saber qué falta cuadrar. Mismo espíritu que `Guia.bloqueo_ponderaciones()` (que sí bloquea el envío a revisión, pero es un medidor de mensaje, no una excepción) -- aquí ni siquiera hay envío que bloquear, es puramente informativo.

Sin `<<choice>>` -- no hay rama de fallo, solo la presentación del estado. Verbo `consultar` ya existente en el catálogo (`consultarEstadoGuias()` es el precedente exacto: un `read` que agrega estado y lo presenta), forma relajada `consultarEstado...()`.

No se valida la suma total de `horas` contra los `ECTS` de la `AsignaturaGrado`/`Materia` -- solo la regla `AfM = Σ AfAdM` (decisión de Manuel en la discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : consultarEstadoActividadesFormativasMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas}`, `ActividadFormativaAsignaturaGrado{horas, porcentajePresencialidad}`; README: "Regla `AfM = Σ AfAdM`: validación blanda a nivel de `Materia`"
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) / [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) -- los dos repartos que este medidor contrasta
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo `consultarEstado...()`
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas y decisión de la validación blanda
