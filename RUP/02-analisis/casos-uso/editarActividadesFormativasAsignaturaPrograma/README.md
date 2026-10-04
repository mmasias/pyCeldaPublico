<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadesFormativasAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md): mismo patrón que [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) sobre la asociación `ActividadFormativaAsignaturaPrograma`, con dos campos editables por fila (`horas` y `porcentajePresencialidad`, este último en rango 0-100). `<<choice>>` de validación de entrada: `horas` negativas o `porcentajePresencialidad` fuera de `[0, 100]` -> no se guarda nada. Es este nivel el que el render de la `Guia` consume (sección 4 del formulario oficial).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadesFormativasAsignaturaProgramaView`

**Responsabilidades:**
- presenta las 10 `ActividadFormativa` (`codigo`/`nombre` de solo lectura) con sus `horas` y `porcentajePresencialidad` actuales editables.
- ofrece la navegación a solicitar guardar el reparto completo.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita editar las actividades formativas de la `AsignaturaPrograma`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO` (reparto guardado, o valor no válido -- no se guarda nada).

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- recupera el reparto actual (`cargarActividadesFormativas(asignaturaProgramaId)`).
- valida cada fila: `horas >= 0` y `0 <= porcentajePresencialidad <= 100`; si alguna falla, rechaza el guardado completo.
- aplica el nuevo reparto (`guardarActividadesFormativas(asignaturaProgramaId, reparto)`) fila a fila y persiste el lote.

**Colaboraciones:**
- **Entrada:** `EditarActividadesFormativasAsignaturaProgramaView`.
- **Salida:** `ActividadFormativaAsignaturaProgramaRepository`.

## Clases de modelo

### `ActividadFormativaAsignaturaPrograma`

**Responsabilidades:**
- actualiza sus `horas` y `porcentajePresencialidad` (`actualizar(horas, porcentajePresencialidad)`). Las 10 filas existen siempre (autopobladas a 0 al crear la `AsignaturaPrograma`), no se crean ni se borran aquí.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `ActividadFormativaAsignaturaProgramaRepository`.

### `ActividadFormativaAsignaturaProgramaRepository`

**Responsabilidades:**
- recupera las 10 filas de asociación de una `AsignaturaPrograma` (`listarDe(asignaturaProgramaId)`).
- persiste el lote de cambios (`actualizarLote(actividadesFormativasAsignaturaPrograma)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `ActividadFormativaAsignaturaPrograma`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarActividadesFormativasAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaPrograma{horas, porcentajePresencialidad}`, `(AsignaturaPrograma, ActividadFormativa) .. ActividadFormativaAsignaturaPrograma`.
- [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) -- medidor que contrasta la suma de estas `horas` contra las de la materia.
