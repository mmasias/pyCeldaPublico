<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): un solo paso, de solo lectura. Presenta `codigo` y `nombre` y ofrece la edición. A diferencia de [`abrirCompetencia()`](../abrirCompetencia/README.md), no hay colaboración de asignaciones: con el autopoblado todas las `Materia` y `AsignaturaPrograma` del programa tienen fila para la actividad, así que una lista de "dónde está asignada" no informaría de nada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirActividadFormativaView`

**Responsabilidades:**
- presenta los datos de la `ActividadFormativa`: `codigo` y `nombre`.
- permite solicitar editar o volver al catálogo del programa.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` -- el actor abre una actividad del catálogo.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDAD_FORMATIVA_ABIERTO`.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- carga la `ActividadFormativa` (`cargarActividadFormativa(actividadFormativaId)`).

**Colaboraciones:**
- **Entrada:** `AbrirActividadFormativaView`.
- **Salida:** `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- porta `codigo` y `nombre`, y el `Programa` al que pertenece.

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- recupera la `ActividadFormativa` por identificador (`obtener(actividadFormativaId)`).

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/wireframes.puml) -- fuente de verdad de la ficha de solo lectura.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo del `Programa`.
- [`abrirCompetencia()`](../abrirCompetencia/README.md) -- contraste: ficha con distribución.
