<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/README.md): edita los 8 atributos propios de una vez, con un `<<choice>>` que bifurca solo la presentación del campo `semestreDefault` (bloqueado si ya existe alguna `Guia` para esta `AsignaturaGrado`), no el caso de uso entero. Único caso de edición del catálogo que no es de `Admin`. El 8.º atributo es `requisitosPrevios` (texto plano, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)), en la misma familia de campo de override que `contenido`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarAsignaturaGradoView`

**Responsabilidades:**
- presenta los 8 campos editables (`curso`, `caracter`, `idioma`, `semestreDefault`, `nombre`, `ects`, `contenido`, `requisitosPrevios`) con sus valores actuales.
- muestra `semestreDefault` bloqueado, con su motivo, cuando `semestreDefaultBloqueado` es verdadero.
- ofrece la navegación a solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita editar la `AsignaturaGrado`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- recupera la `AsignaturaGrado` a editar y determina si `semestreDefault` está bloqueado (`obtenerParaEditar(asignaturaGradoId)`).
- aplica los cambios confirmados (`guardarCambios(asignaturaGradoId, curso, caracter, idioma, semestreDefault, nombre, ects, contenido, requisitosPrevios)`).

**Colaboraciones:**
- **Entrada:** `EditarAsignaturaGradoView`.
- **Salida:** `AsignaturaGrado`, `AsignaturaGradoRepository`, `GuiaRepository`.

## Clases de modelo

### `AsignaturaGrado`

**Responsabilidades:**
- actualiza sus 8 atributos propios (`actualizar(curso, caracter, idioma, semestreDefault, nombre, ects, contenido, requisitosPrevios)`); aplica `semestreDefault` solo si no llega bloqueado -- protección de la invariante en el propio Modelo, no solo en la Vista.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- recupera la `AsignaturaGrado` por identificador (`obtener(asignaturaGradoId)`).
- persiste los cambios (`actualizar(asignaturaGrado)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `GuiaRepository`

**Responsabilidades:**
- verifica si existe alguna `Guia` para esta `AsignaturaGrado` (`existeAlgunaDe(asignaturaGradoId)`) -- base del `<<choice>>` que bloquea `semestreDefault`.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Guia` (ya introducido por el hilo `Guia`, reutilizado aquí sin duplicar).

## `<<choice>>` sobre `semestreDefault`, resuelto en Requisitos (2026-08-19)

Requisitos dejaba este caso de uso deliberadamente **sin** `<<choice>>` de bloqueo sobre `semestreDefault`, con nota explícita de revisión al cerrar L7-L9. Con el hilo `Guia` ya cerrado en Desarrollo (PR [#68](https://github.com/mmasias/pyCelda/pull/68)), la condición -- "¿existe ya alguna `Guia` para esta `AsignaturaGrado`?" -- es comprobable, y el `<<choice>>` se formalizó en Requisitos (ver [especificación actualizada](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/especificacion.puml)). **No bloquea el caso de uso entero** -- a diferencia de `editarCursoAcademico()`, aquí solo un campo de ocho es condicionalmente invariante, así que el `<<choice>>` bifurca la consulta previa (`obtenerParaEditar`) que decide qué presenta la Vista, no el flujo de guardado. La protección real de la invariante vive en `AsignaturaGrado.actualizar()` (Fat Model): aunque el cliente forzara un valor distinto de `semestreDefault` con el campo bloqueado, el Modelo lo ignora -- no basta con que la Vista no lo ofrezca.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/wireframes.puml) -- fuente de verdad, con el `<<choice>>` ya formalizado.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : editarAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`; README, invarianza condicional de `semestreDefault`, `requisitosPrevios` texto plano en vivo (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)).
- [`editarSemestreGuia()`](../editarSemestreGuia/README.md) -- caso de uso análogo ya cerrado sobre `Guia.semestre`, mismo patrón de campo editable sin `HistorialCambio`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- primer caso de uso de este lote que ya reutilizó un Repository del hilo `Guia` (`GuiaRepository.listarDelGrado()`); este CU repite el mismo criterio con `GuiaRepository.existeAlgunaDe()`.
