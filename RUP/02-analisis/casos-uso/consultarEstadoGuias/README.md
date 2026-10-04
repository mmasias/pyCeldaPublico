<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoGuias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`consultarEstadoGuias()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de `Guia` del `Programa` con su `AsignaturaPrograma`, profesorado y estado. Compartido entre `DirectorPrograma` (entrada al ciclo de revisión: alcanza [`abrirGuia()`](../abrirGuia/README.md) para decidir sobre cada una) y `Admin` (monitoreo de la beta: alcanza [`previsualizarGuia()`](../previsualizarGuia/README.md) y [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md), no `abrirGuia()` -- issue [#262](https://github.com/mmasias/pyCelda/issues/262)). Autorización de "admin **o** dirige el programa", `404` uniforme -- el mismo camino que resuelve el gate en el Modelo/Controlador, no una rama de validación.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/consultarEstadoGuias/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ConsultarEstadoGuiasView`

**Responsabilidades:**
- presenta el listado de `Guia` del `Programa`: `AsignaturaPrograma`, profesorado y `estado` de cada una.
- según el actor, ofrece por fila la navegación a `abrirGuia()` (`DirectorPrograma`) o a `previsualizarGuia()`/`descargarGuiaPDF()` (`Admin`); el `Admin` no ve `abrirGuia()` ni `notificarGuiasActualizadas()`.
- la vuelta al `Programa` la resuelve la navegación común de cada actor (`NavPrograma` para `DirectorPrograma`, "Volver" de `ProgramaAdmin` para `Admin`), no un botón propio.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `DirectorPrograma` o el `Admin` solicita consultar el estado de las `Guia` del `Programa`.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_PROGRAMA_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- lista las `Guia` del `Programa` (`listarGuiasDelPrograma(programaId)`) -- método nuevo, primer listado agregado de `Guia` de la rebanada (los ocho casos ya construidos operan siempre sobre una `Guia` ya identificada). Con #254, la carga anticipada incluye `asignaturaPrograma.profesorado` para la columna en vivo.
- resuelve la autorización antes de listar: **admin o dirige el programa** (`Admin` -> siempre; `DirectorPrograma` -> solo sus programas), `404` uniforme si no -- mismo patrón que `descargarGuiaPDF()`/`previsualizarGuia()`.
- por fila expone si la `Guia` tiene PDF generado (`tienePdf`, issue [#262](https://github.com/mmasias/pyCelda/issues/262)), dato que la Vista usa para habilitar o no el botón `[Descargar PDF]` de la variante `Admin`.
- no valida ni muta nada más -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `ConsultarEstadoGuiasView`.
- **Salida:** `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- porta `estado` y su `AsignaturaPrograma` asociada -- los datos mostrados en cada fila del listado. El profesorado de cada fila se lee de `asignaturaPrograma.profesorado` **en vivo** (issue [#254](https://github.com/mmasias/pyCelda/issues/254)), no de la copia `Guia -- Profesor` -- misma fuente que [`abrirGuia()`](../abrirGuia/README.md).
- expone `ultimaActualizacion`/`ultimaActualizacionRol` para la columna "Última actualización"; con #254 `ultimaActualizacionRol` puede valer "Administración" (transición `Aprobada -> EnRevision` con `autor` centinela).
- responde si tiene su PDF generado (`tienePdfGenerado()`, a partir de si `fechaGeneracionPDF` está vacía -- misma consulta que ya usa `descargarGuiaPDF()`), para la variante `Admin` del listado (issue [#262](https://github.com/mmasias/pyCelda/issues/262)).

**Colaboraciones:**
- **Entrada:** listada por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- lista las `Guia` del `Programa` (`listarDelPrograma(programaId)`) -- método nuevo, recorre la cascada `Programa`->`Materia`->`AsignaturaPrograma`->`Guia` del `CursoAcademico` activo.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> GUIAS_DEL_PROGRAMA_ABIERTO : consultarEstadoGuias()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia` como clase de asociación de `(AsignaturaPrograma, CursoAcademico)`.
- [`abrirGuia()`](../abrirGuia/README.md) -- caso de uso alcanzado desde cada fila de este listado, contexto de revisión.
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- self-loop sobre el mismo `:GUIAS_DEL_PROGRAMA_ABIERTO` que esta pantalla presenta.
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- profesorado del listado en vivo; `ultimaActualizacionRol` gana "Administración".
