<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadesFormativasAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md): mismo patrón que [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) sobre la asociación `ActividadFormativaAsignaturaPrograma`, con un solo campo editable por fila: `horas`. Desde el issue [#772](https://github.com/mmasias/pyCelda/issues/772) la presencialidad vive en la `Materia` (`ActividadFormativaMateria`): el controlador la lee de allí para presentarla de solo lectura junto a cada fila. `<<choice>>` de validación de entrada: `horas` negativas -> no se guarda nada. Es este nivel el que el render de la `Guia` consume para las horas (sección 4 del formulario oficial), con la presencialidad de la `Materia`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadesFormativasAsignaturaProgramaView`

**Responsabilidades:**
- presenta las `ActividadFormativa` del catálogo del `Programa` (`codigo`/`nombre` de solo lectura) con sus `horas` actuales editables.
- presenta, de solo lectura, el `porcentajePresencialidad` de cada actividad en la `Materia` de la asignatura.
- presenta el total de horas frente a 25 h por ECTS de la `AsignaturaPrograma`, si tiene `ects`, y lo recalcula mientras se introducen las horas, antes de guardar (informativo, issue [#786](https://github.com/mmasias/pyCelda/issues/786); mismo cálculo que `AsignaturaPrograma.comprobacionHorasEcts()` de [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md), sobre las horas tecleadas).
- ofrece la navegación a solicitar guardar el reparto completo.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita editar las actividades formativas de la `AsignaturaPrograma`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO` (reparto guardado, o horas negativas -- no se guarda nada).

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- recupera el reparto actual (`cargarActividadesFormativas(asignaturaProgramaId)`), con la presencialidad de la `Materia` de la asignatura.
- valida cada fila: `horas >= 0`; si alguna falla, rechaza el guardado completo. Una presencialidad recibida no se aplica: no es un dato de este nivel.
- aplica el nuevo reparto (`guardarActividadesFormativas(asignaturaProgramaId, repartoHoras)`) fila a fila y persiste el lote.

**Colaboraciones:**
- **Entrada:** `EditarActividadesFormativasAsignaturaProgramaView`.
- **Salida:** `ActividadFormativaAsignaturaProgramaRepository`.

## Clases de modelo

### `ActividadFormativaAsignaturaPrograma`

**Responsabilidades:**
- actualiza sus `horas` (`actualizar(horas)`) -- único campo de la asociación. Las filas existen siempre, una por cada actividad del catálogo del `Programa` (autopobladas a 0 al crear la `AsignaturaPrograma` o la actividad), no se crean ni se borran aquí.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `ActividadFormativaAsignaturaProgramaRepository`.

### `ActividadFormativaAsignaturaProgramaRepository`

**Responsabilidades:**
- recupera las filas de asociación de una `AsignaturaPrograma` (`listarDe(asignaturaProgramaId)`), en el orden de alta del catálogo.
- persiste el lote de cambios (`actualizarLote(actividadesFormativasAsignaturaPrograma)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `ActividadFormativaAsignaturaPrograma`.

### `ActividadFormativaMateria`

**Responsabilidades:**
- porta el `porcentajePresencialidad` de cada actividad en la `Materia` (#772), que este caso de uso presenta sin modificar.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, solo lectura.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarActividadesFormativasAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaPrograma{horas}`, `(AsignaturaPrograma, ActividadFormativa) .. ActividadFormativaAsignaturaPrograma`; `ActividadFormativaMateria{horas, porcentajePresencialidad}`.
- [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) -- medidor que contrasta la suma de estas `horas` contra las de la materia.
