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

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`|
|**Objetivo**|Consultar el estado de la regla `AfM = Σ AfAdM` de una `Materia`: por cada `ActividadFormativa`, las `horas` de la materia frente a la suma de las de sus `AsignaturaPrograma`, con las discrepancias marcadas|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Medidor de la regla **`AfM = Σ AfAdM`** (actividades formativas de la materia = suma de las de sus asignaturas). Se compone desde [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md) -- self-loop de `MATERIA_ABIERTO`, mismo patrón que `previsualizarGuia()` sobre `GUIA_ABIERTO` (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)): un CU propio, de solo lectura, que otra pantalla incrusta.

**Validación blanda, no un gate**: presenta las 10 actividades formativas con `horas` de la materia (`ActividadFormativaMateria`), la suma de `horas` de sus `AsignaturaPrograma` (`ActividadFormativaAsignaturaPrograma`) y la diferencia; marca las que no cuadran. **No bloquea ningún guardado** -- ni el de [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) ni el de [`editarActividadesFormativasAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md). El `DirectorPrograma` construye el reparto de forma incremental y usa el medidor para saber qué falta cuadrar. Mismo espíritu que `Guia.bloqueo_ponderaciones()` (que sí bloquea el envío a revisión, pero es un medidor de mensaje, no una excepción) -- aquí ni siquiera hay envío que bloquear, es puramente informativo.

Sin `<<choice>>` -- no hay rama de fallo, solo la presentación del estado. Verbo `consultar` ya existente en el catálogo (`consultarEstadoGuias()` es el precedente exacto: un `read` que agrega estado y lo presenta), forma relajada `consultarEstado...()`.

No se valida la suma total de `horas` contra los `ECTS` de la `AsignaturaPrograma`/`Materia` -- solo la regla `AfM = Σ AfAdM` (decisión de Manuel en la discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : consultarEstadoActividadesFormativasMateria()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas}`, `ActividadFormativaAsignaturaPrograma{horas, porcentajePresencialidad}`; README: "Regla `AfM = Σ AfAdM`: validación blanda a nivel de `Materia`"
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) / [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- los dos repartos que este medidor contrasta
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo `consultarEstado...()`
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas y decisión de la validación blanda
