<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Editar las `horas` y el `porcentajePresencialidad` del reparto de las 10 `ActividadFormativa` de una `AsignaturaGrado` (`ActividadFormativaAsignaturaGrado`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo caso de uso que [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md) un escalón más abajo en la cascada `Materia` -> `AsignaturaGrado`, con **un campo más**: además de `horas` (decimales), cada actividad formativa lleva `porcentajePresencialidad` en rango **0-100** (con validación). El `DirectorGrado` teclea los 10 pares (`horas`, `%`) en una rejilla y guarda de una sola vez. Las 10 filas están siempre presentes, autopobladas a 0 al crear la `AsignaturaGrado`; sin `asociar`/`desasociar`. `codigo`/`nombre` de cada `ActividadFormativa` de solo lectura (catálogo institucional).

`<<choice>>` tras la entrada de datos: rojo si alguna `horas` es negativa o algún `porcentajePresencialidad` cae fuera de `[0, 100]` -- rechaza el guardado completo y vuelve a `ASIGNATURA_GRADO_ABIERTO` sin escribir nada. Verde persiste las 10 filas.

Es este nivel (`AsignaturaGrado`) el que consume el render de la `Guia`: `descargarGuiaPDF()`/`previsualizarGuia()` pintan las 10 filas de `(AsignaturaGrado, ActividadFormativa)` con sus `horas` y `%` en la sección 4 del formulario oficial. El `Profesor` **no** ve ni edita esta tabla en ninguna pantalla -- solo aparece en el render de su guía, igual que las metodologías docentes y los resultados de aprendizaje.

Retoca [`abrirAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/README.md): la pantalla de detalle de `AsignaturaGrado` gana la sección "Actividades formativas" con la rejilla y el botón de entrada, sin tocar su especificación.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : editarActividadesFormativasAsignaturaGrado()` (verde y rojo al mismo estado)
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaGrado{horas, porcentajePresencialidad}`, `(AsignaturaGrado, ActividadFormativa) .. ActividadFormativaAsignaturaGrado`
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) -- el mismo reparto en el nivel `Materia`, contra el que se contrasta la regla `AfM = Σ AfAdM`
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) / [`previsualizarGuia()`](../previsualizarGuia/README.md) -- consumidores del reparto en el render de la guía
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- requerimiento de las actividades formativas
