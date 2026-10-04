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
|**Objetivo**|Editar las `horas` y el `porcentajePresencialidad` del reparto de las 10 `ActividadFormativa` de una `AsignaturaPrograma` (`ActividadFormativaAsignaturaPrograma`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo caso de uso que [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) un escalón más abajo en la cascada `Materia` -> `AsignaturaPrograma`, con **un campo más**: además de `horas` (decimales), cada actividad formativa lleva `porcentajePresencialidad` en rango **0-100** (con validación). El `DirectorPrograma` teclea los 10 pares (`horas`, `%`) en una rejilla y guarda de una sola vez. Las 10 filas están siempre presentes, autopobladas a 0 al crear la `AsignaturaPrograma`; sin `asociar`/`desasociar`. `codigo`/`nombre` de cada `ActividadFormativa` de solo lectura (catálogo institucional).

`<<choice>>` tras la entrada de datos: rojo si alguna `horas` es negativa o algún `porcentajePresencialidad` cae fuera de `[0, 100]` -- rechaza el guardado completo y vuelve a `ASIGNATURA_PROGRAMA_ABIERTO` sin escribir nada. Verde persiste las 10 filas.

Es este nivel (`AsignaturaPrograma`) el que consume el render de la `Guia`: `descargarGuiaPDF()`/`previsualizarGuia()` pintan las 10 filas de `(AsignaturaPrograma, ActividadFormativa)` con sus `horas` y `%` en la sección 4 del formulario oficial. El `Profesor` **no** ve ni edita esta tabla en ninguna pantalla -- solo aparece en el render de su guía, igual que las metodologías docentes y los resultados de aprendizaje.

Retoca [`abrirAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md): la pantalla de detalle de `AsignaturaPrograma` gana la sección "Actividades formativas" con la rejilla y el botón de entrada, sin tocar su especificación.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarActividadesFormativasAsignaturaPrograma()` (verde y rojo al mismo estado)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaPrograma{horas, porcentajePresencialidad}`, `(AsignaturaPrograma, ActividadFormativa) .. ActividadFormativaAsignaturaPrograma`
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) -- el mismo reparto en el nivel `Materia`, contra el que se contrasta la regla `AfM = Σ AfAdM`
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) / [`previsualizarGuia()`](../previsualizarGuia/README.md) -- consumidores del reparto en el render de la guía
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas
