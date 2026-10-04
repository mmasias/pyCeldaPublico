<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSemestreGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarSemestreGuia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarSemestreGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/README.md): el `DirectorPrograma` edita el `semestre` de la `Guia` abierta, disponible sin condición de `estado` (a diferencia de las decisiones de revisión). Sin `<<choice>>` ni `HistorialCambio` -- la especificación no los pide. El único matiz es un efecto colateral condicional: si la `Guia` estaba `Aprobada`, el cambio de semestre regenera su PDF y actualiza `fechaGeneracionPDF`, sin transición de estado (a diferencia de [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md), que sí dispara `Aprobada -> Borrador`).

**Ya no es el único disparador de `regenerarPDF()`** (retoque posterior, discussion [#224](https://github.com/mmasias/pyCelda/discussions/224)): `aprobarGuia()`/`escalarGuiaAAprobada()` lo llaman también, como parte de su propio cambio de estado. Este caso de uso no cambia en nada -- sigue regenerando el PDF bajo la misma condición (`estado == Aprobada` en el momento de editar), es simplemente uno de varios disparadores en vez de el único. Nace precisamente porque, antes de este retoque, era el único punto que lo hacía -- de ahí el workaround real que Manuel usaba ("editar semestre y guardar" para forzar la regeneración tras aprobar).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarSemestreGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarSemestreGuiaView`

**Responsabilidades:**
- presenta el `semestre` actual de la `Guia`.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `DirectorPrograma` solicita editar el semestre de la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIA_ABIERTO` -- self-loop.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- pide a la `Guia` que actualice su `semestre` y, condicionalmente, que regenere su PDF; persiste el agregado.
- no valida ni registra `HistorialCambio` -- la especificación no modela ninguna de las dos cosas para este caso de uso.

**Colaboraciones:**
- **Entrada:** `EditarSemestreGuiaView`.
- **Salida:** `Guia`, `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- actualiza su propio `semestre` (`actualizarSemestre(semestre)`).
- regenera su PDF (`regenerarPDF()`) solo si su `estado` era `Aprobada` en el momento de la edición -- actualiza `fechaGeneracionPDF`, sin transición de `estado`.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- persiste de verdad el agregado (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/wireframes.puml) -- fuente de verdad de la regeneración condicional de PDF.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : editarSemestreGuia()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia{semestre, fechaGeneracionPDF}`.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- contraste: su efecto colateral sí dispara transición de estado (`Aprobada -> Borrador`), este caso no.
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- consumidor de `fechaGeneracionPDF`, actualizado aquí cuando aplica (y, desde el retoque de discussion #224, también por `aprobarGuia()`/`escalarGuiaAAprobada()`).
- [`aprobarGuia()`](../aprobarGuia/README.md) / [`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md) -- disparadores nuevos del mismo `regenerarPDF()`, discussion [#224](https://github.com/mmasias/pyCelda/discussions/224).
