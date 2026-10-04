<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/README.md): edita los 8 atributos propios de una vez, con un `<<choice>>` que bifurca solo la presentación del campo `semestreDefault` (bloqueado si ya existe alguna `Guia` para esta `AsignaturaPrograma`), no el caso de uso entero. Único caso de edición del catálogo, compartido por `DirectorPrograma` y `Admin` (issue [#602](https://github.com/mmasias/pyCelda/issues/602)). El 8.º atributo es `requisitosPrevios` (texto plano, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)), en la misma familia de campo de override que `contenido`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarAsignaturaProgramaView`

**Responsabilidades:**
- presenta los 8 campos editables (`curso`, `caracter`, `idioma`, `semestreDefault`, `nombre`, `ects`, `contenido`, `requisitosPrevios`) con sus valores actuales.
- muestra `semestreDefault` bloqueado, con su motivo, cuando `semestreDefaultBloqueado` es verdadero.
- ofrece la navegación a solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el actor (`DirectorPrograma` o `Admin`) solicita editar la `AsignaturaPrograma`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- recupera la `AsignaturaPrograma` a editar y determina si `semestreDefault` está bloqueado (`obtenerParaEditar(asignaturaProgramaId)`).
- aplica los cambios confirmados (`guardarCambios(asignaturaProgramaId, curso, caracter, idioma, semestreDefault, nombre, ects, contenido, requisitosPrevios)`).

**Colaboraciones:**
- **Entrada:** `EditarAsignaturaProgramaView`.
- **Salida:** `AsignaturaPrograma`, `AsignaturaProgramaRepository`, `GuiaRepository`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- actualiza sus 8 atributos propios (`actualizar(curso, caracter, idioma, semestreDefault, nombre, ects, contenido, requisitosPrevios)`); aplica `semestreDefault` solo si no llega bloqueado -- protección de la invariante en el propio Modelo, no solo en la Vista.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- recupera la `AsignaturaPrograma` por identificador (`obtener(asignaturaProgramaId)`).
- persiste los cambios (`actualizar(asignaturaPrograma)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `GuiaRepository`

**Responsabilidades:**
- verifica si existe alguna `Guia` para esta `AsignaturaPrograma` (`existeAlgunaDe(asignaturaProgramaId)`) -- base del `<<choice>>` que bloquea `semestreDefault`.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Guia` (ya introducido por el hilo `Guia`, reutilizado aquí sin duplicar).

## `<<choice>>` sobre `semestreDefault`, resuelto en Requisitos (2026-08-19)

Requisitos dejaba este caso de uso deliberadamente **sin** `<<choice>>` de bloqueo sobre `semestreDefault`, con nota explícita de revisión al cerrar L7-L9. Con el hilo `Guia` ya cerrado en Desarrollo (PR [#68](https://github.com/mmasias/pyCelda/pull/68)), la condición -- "¿existe ya alguna `Guia` para esta `AsignaturaPrograma`?" -- es comprobable, y el `<<choice>>` se formalizó en Requisitos (ver [especificación actualizada](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/especificacion.puml)). **No bloquea el caso de uso entero** -- a diferencia de `editarCursoAcademico()`, aquí solo un campo de ocho es condicionalmente invariante, así que el `<<choice>>` bifurca la consulta previa (`obtenerParaEditar`) que decide qué presenta la Vista, no el flujo de guardado. La protección real de la invariante vive en `AsignaturaPrograma.actualizar()` (Fat Model): aunque el cliente forzara un valor distinto de `semestreDefault` con el campo bloqueado, el Modelo lo ignora -- no basta con que la Vista no lo ofrezca.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/wireframes.puml) -- fuente de verdad, con el `<<choice>>` ya formalizado.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`; README, invarianza condicional de `semestreDefault`, `requisitosPrevios` texto plano en vivo (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)).
- [`editarSemestreGuia()`](../editarSemestreGuia/README.md) -- caso de uso análogo ya cerrado sobre `Guia.semestre`, mismo patrón de campo editable sin `HistorialCambio`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- primer caso de uso de este lote que ya reutilizó un Repository del hilo `Guia` (`GuiaRepository.listarDelPrograma()`); este CU repite el mismo criterio con `GuiaRepository.existeAlgunaDe()`.
