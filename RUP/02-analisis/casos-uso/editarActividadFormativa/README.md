<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`editarActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): CRUD real e inmediato con el `<<choice>>` de código repetido de [`editarCompetencia()`](../editarCompetencia/README.md). `codigo` y `nombre` editables; la comprobación de unicidad excluye a la propia actividad (`salvo`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadFormativaView`

**Responsabilidades:**
- presenta los datos actuales: `codigo` y `nombre`, los dos obligatorios.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDAD_FORMATIVA_ABIERTO`.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDAD_FORMATIVA_ABIERTO` con los datos actualizados.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- carga la `ActividadFormativa` (`cargarActividadFormativa(actividadFormativaId)`).
- valida que el `codigo` no lo use otra actividad formativa del mismo `Programa`.
- actualiza el modelo y persiste.

**Colaboraciones:**
- **Entrada:** `EditarActividadFormativaView`.
- **Salida:** `ActividadFormativa`, `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- se actualiza a sí misma (`actualizar(codigo, nombre)`); su `Programa` no cambia.

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`; mutada por `ActividadFormativaController`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- responde si un `codigo` está en uso en el `Programa`, salvo la propia (`codigoEnUso(programaId, codigo, salvo)`).
- persiste la editada (`editar(actividadFormativa)`).

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/wireframes.puml) -- fuente de verdad.
- [`editarCompetencia()`](../editarCompetencia/README.md) -- patrón de origen.
