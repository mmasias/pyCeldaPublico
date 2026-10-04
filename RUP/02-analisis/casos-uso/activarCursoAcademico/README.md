<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > activarCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`activarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md): combina el patrón `<<choice>>` bloqueante de [`eliminarFacultad()`](../eliminarFacultad/README.md) (acción de conjunto, self-loop sobre el listado, sin pantalla de confirmación intermedia) con el efecto colateral de creación masiva de [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md) -- pero aquí no es una `Guia`, son todas: una por cada `AsignaturaPrograma` con `estado="Activo"` de la institución. Es el caso de uso de mayor alcance del catálogo: segunda mitad de [#222](https://github.com/mmasias/pyCelda/issues/222) (la primera, [`crearCursoAcademico()`](../crearCursoAcademico/README.md), ya construida).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/activarCursoAcademico/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ActivarCursoAcademicoView`

**Responsabilidades:**
- en la rama verde, presenta el `CursoAcademico` activado y la lista actualizada.
- en la rama roja, presenta el mensaje de bloqueo.

**Colaboraciones:**
- **Entrada:** `:CURSOS_ACADEMICOS_ABIERTO` -- el `Admin` solicita activar un `CursoAcademico` desde el listado (botón `[Activar]`, que ya no se ofrece en candidatos siempre bloqueados -- ver [`abrirCursosAcademicos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md)).
- **Control:** `CursoAcademicoController`.
- **Salida:** `:CURSOS_ACADEMICOS_ABIERTO` en ambos casos -- "activado, lista actualizada" (verde) o "bloqueado, sin cambios" (rojo).

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- aplica el `<<choice>>` de elegibilidad (discussion [#15](https://github.com/mmasias/pyCelda/discussions/15)): el último `CursoAcademico` (por id, siempre que esté Inactivo) o el penúltimo (solo si además el último no tiene actividad registrada -- alguna fila de `HistorialCambio` asociada a alguna de sus `Guia`).
- si es elegible, delega el efecto completo (`activarCursoAcademico(cursoAcademicoId)`) en `CursoAcademicoRepository`.

**Colaboraciones:**
- **Entrada:** `ActivarCursoAcademicoView`.
- **Salida:** `CursoAcademicoRepository`, `HistorialCambio`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `estado` -- pasa a `Inactivo` el que lo estaba, a `Activo` el elegido. Nunca hay dos `Activo` a la vez.

### `CursoAcademicoRepository`

**Responsabilidades:**
- responde `ultimo()`/`penultimo()` (orden de alta, id ascendente) -- origen de la regla de elegibilidad.
- aplica la activación completa (`activar(cursoAcademicoId)`): desactiva el `Activo` anterior, activa el elegido, y por cada `AsignaturaPrograma` Activo de la institución crea una `Guia` nueva -- clonando de la `Guia` del curso que queda desactivado si existe para esa `AsignaturaPrograma`, o derivando de la propia `AsignaturaPrograma` si no. Transacción única.

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`, `AsignaturaPrograma`, `Guia`.

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `semestreDefault`/`contenido`/`sesionesMinimas`/`profesorado` -- semilla de la `Guia` nueva cuando no hay una anterior que clonar (mismas reglas de herencia que `crearAsignaturaPrograma()`); `profesorado` se lee siempre en vivo, se clone o no la `Guia` (nunca se copia del año anterior). Las `Extinguido` no reciben alta nueva -- "Extinguido bloquea altas nuevas" ([modelo del dominio](/RUP/00-modelo-del-dominio/README.md)).

### `Guia`

**Responsabilidades:**
- nace siempre `estado="Borrador"`, con `cursoAcademicoId` del curso recién activado. Si existe una `Guia` de la misma `AsignaturaPrograma` en el curso que queda desactivado, clona `semestre`/`contenido`/`textoSistemaEvaluacion`/`sesionesMinimas` de ella; si no, `semestre`/`contenido`/`sesionesMinimas` los toma de `AsignaturaPrograma` y `textoSistemaEvaluacion` nace vacío (`""`, sin semilla). `fechaCreacion`/`fechaUltimaModificacion`/`fechaGeneracionPdf`/`historial` nacen siempre frescos -- nunca clonados (ninguna columna nacida después del cierre original del contrato en discussion [#47](https://github.com/mmasias/pyCelda/discussions/47) lo cambia, reverificado en discussion [#430](https://github.com/mmasias/pyCelda/discussions/430)).

### `PonderacionEvaluacion` / `ReferenciaBibliografica`

**Responsabilidades:**
- si hay `Guia` anterior que clonar, cada `PonderacionEvaluacion`/`ReferenciaBibliografica` vinculada al efecto se copia como fila nueva (mismo campo `vinculada` replicado, no forzado) -- copias reales, no referencias compartidas. Si no hay `Guia` anterior, la nueva nace sin ninguna.

### `HistorialCambio`

**Responsabilidades:**
- el `<<choice>>` consulta si el último `CursoAcademico` tiene alguna fila asociada a alguna de sus `Guia` -- "actividad registrada" que bloquea la reactivación del penúltimo.

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.

## Fuera de alcance de esta rebanada

`Sesion` (planificación docente real, no confundir con `sesionesMinimas`) **nunca se clona** -- ni la especificación ni el cierre de discussion #430 la incluyen en el contrato: cada curso académico replanifica desde cero. `activarSemestre()` (`CursoAcademico.semestreActivo`) tampoco está en el alcance de este caso de uso.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/wireframes.puml).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSOS_ACADEMICOS_ABIERTO --> CURSOS_ACADEMICOS_ABIERTO : activarCursoAcademico()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- regla de elegibilidad completa, contrato de clonado de `Guia`.
- [`eliminarFacultad()` en Análisis](../eliminarFacultad/README.md) -- plantilla del `<<choice>>` bloqueante, acción de conjunto sin abrir un elemento antes.
- [`crearAsignaturaPrograma()` en Análisis](../crearAsignaturaPrograma/README.md) -- plantilla del efecto colateral de nacimiento de `Guia`, aquí multiplicado por cada `AsignaturaPrograma` de la institución.
- [`crearCursoAcademico()`](../crearCursoAcademico/README.md) -- primera mitad de #222, ya construida.
