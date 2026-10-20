<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))|
|**Objetivo**|Editar las `horas` del reparto de las actividades formativas de una `AsignaturaPrograma` (`ActividadFormativaAsignaturaPrograma`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo caso de uso que [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) un escalón más abajo en la cascada `Materia` -> `AsignaturaPrograma`, **solo con `horas`** (decimales). El `DirectorPrograma` teclea las horas de cada actividad formativa en una rejilla y guarda de una sola vez. La rejilla tiene una fila por cada `ActividadFormativa` del catálogo del `Programa` de la asignatura, siempre presente: se crea a 0 al dar de alta la `AsignaturaPrograma` o la actividad (invariante de autopoblado); sin `asociar`/`desasociar`. `codigo`/`nombre` de cada actividad de solo lectura (catálogo del `Programa`).

**Presencialidad de solo lectura, la de la `Materia`** (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): la rejilla presenta, junto a las horas, el porcentaje de presencialidad que la `Materia` fija para cada actividad ([`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md)). No se edita aquí: la memoria lo fija por materia, y con la presencialidad en la asignatura cada `AsignaturaPrograma` podía declarar una distinta. Hasta #772 esta rejilla editaba `horas` y `porcentajePresencialidad` y el `<<choice>>` validaba también el rango 0-100.

`<<choice>>` tras la entrada de datos: rojo si alguna `horas` es negativa -- rechaza el guardado completo y vuelve a `ASIGNATURA_PROGRAMA_ABIERTO` sin escribir nada. Verde persiste todas las filas.

Es este nivel (`AsignaturaPrograma`) el que consume el render de la `Guia` para las horas: `descargarGuiaPDF()`/`previsualizarGuia()` pintan las filas de `(AsignaturaPrograma, ActividadFormativa)` con sus `horas` y, al lado, la presencialidad de la `Materia`, en la sección 4 del formulario oficial. El `Profesor` **no** edita esta tabla: la ve de solo lectura en [`abrirGuia()`](../abrirGuia/README.md) y en el render de su guía, igual que las metodologías docentes y los resultados de aprendizaje.

**Total frente a ECTS (issue [#786](https://github.com/mmasias/pyCelda/issues/786))**: si la `AsignaturaPrograma` tiene `ects`, la rejilla presenta bajo la tabla el total de horas frente a 25 h por ECTS, con el mismo formato que la ficha de la asignatura ([`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md)), y lo actualiza mientras se teclean las horas, antes de guardar. Informativo: no entra en el `<<choice>>` ni bloquea el guardado, mismo criterio que el total de [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md). La regla `AfM = Σ AfAdM` sigue sin validarse aquí: vive en [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md).

La misma pantalla ofrece copiar las horas de una asignatura prima de la misma materia ([`importarActividadesFormativasDeAsignaturaProgramaPrima()`](../importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)).

Retoca [`abrirAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md): la pantalla de detalle de `AsignaturaPrograma` gana la sección "Actividades formativas" con la rejilla y el botón de entrada, sin tocar su especificación.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarActividadesFormativasAsignaturaPrograma()` (verde y rojo al mismo estado)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaPrograma{horas}`, `(AsignaturaPrograma, ActividadFormativa) .. ActividadFormativaAsignaturaPrograma`; la presencialidad en `ActividadFormativaMateria{horas, porcentajePresencialidad}`
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) -- el mismo reparto en el nivel `Materia`, contra el que se contrasta la regla `AfM = Σ AfAdM`, y donde se edita la presencialidad
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) / [`previsualizarGuia()`](../previsualizarGuia/README.md) -- consumidores del reparto en el render de la guía
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas; issue [#772](https://github.com/mmasias/pyCelda/issues/772) -- presencialidad en la `Materia`
