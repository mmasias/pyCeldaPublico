<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md): el `DirectorPrograma` edita las `horas` y el `porcentajePresencialidad` de las filas `ActividadFormativaMateria` de una `Materia` -- una por cada `ActividadFormativa` del catálogo de su `Programa` -- en una sola operación (rejilla). `codigo`/`nombre` de cada `ActividadFormativa` se muestran de solo lectura -- catálogo del `Programa`, se edita en [`editarActividadFormativa()`](../editarActividadFormativa/README.md). La presencialidad vive en la `Materia` desde el issue [#772](https://github.com/mmasias/pyCelda/issues/772) (antes, en la `AsignaturaPrograma`). `<<choice>>` de validación de entrada: si alguna `horas` es negativa o alguna presencialidad sale de 0-100, no se guarda nada. El total frente a 25 h por ECTS de la `Materia` es un cálculo de presentación de la vista, sin colaboración propia. La regla `AfM = Σ AfAdM` **no** se comprueba aquí (blanda, vive en [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadesFormativasMateriaView`

**Responsabilidades:**
- presenta las `ActividadFormativa` del catálogo del `Programa` (`codigo`/`nombre` de solo lectura) con sus `horas` y su `porcentajePresencialidad` actuales editables.
- presenta el total de horas frente a 25 h por ECTS de la `Materia`, si tiene `ects` (informativo).
- ofrece la navegación a solicitar guardar el reparto completo.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorPrograma` solicita editar las actividades formativas de la `Materia`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO` (reparto guardado, o algún valor no válido -- no se guarda nada).

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera el reparto actual (`cargarActividadesFormativas(materiaId)`).
- valida que ninguna `horas` sea negativa y que la presencialidad esté entre 0 y 100; si algún valor no lo cumple, rechaza el guardado completo.
- aplica el nuevo reparto (`guardarActividadesFormativas(materiaId, reparto)`) fila a fila y persiste el lote. Una fila sin presencialidad en el reparto conserva la que tenía.

**Colaboraciones:**
- **Entrada:** `EditarActividadesFormativasMateriaView`.
- **Salida:** `ActividadFormativaMateriaRepository`.

## Clases de modelo

### `ActividadFormativaMateria`

**Responsabilidades:**
- actualiza sus `horas` y, si llega, su `porcentajePresencialidad` (`actualizar(horas, porcentajePresencialidad)`) -- los dos campos editables de la asociación. Las filas existen siempre, una por cada actividad del catálogo del `Programa` (autopobladas a 0 al crear la `Materia` o la actividad); no se crean ni se borran aquí.

**Colaboraciones:**
- **Entrada:** `MateriaController`, vía `ActividadFormativaMateriaRepository`.

### `ActividadFormativaMateriaRepository`

**Responsabilidades:**
- recupera las filas de asociación de una `Materia` (`listarDe(materiaId)`), en el orden de alta del catálogo.
- persiste el lote de cambios (`actualizarLote(actividadesFormativasMateria)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `ActividadFormativaMateria`.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` de la `Materia` sea del actor (`Admin` no tiene programa propio).


## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarActividadesFormativasMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas, porcentajePresencialidad}`, `(Materia, ActividadFormativa) .. ActividadFormativaMateria`.
- [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- el mismo patrón un nivel más abajo, solo con `horas`; presenta de solo lectura la presencialidad de esta `Materia`.
