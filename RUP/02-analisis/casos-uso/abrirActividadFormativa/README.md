<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md): un solo paso, de solo lectura. Presenta `codigo` y `nombre` de la `ActividadFormativa` y ofrece la edición. A diferencia de `abrirUniversidad()`, no hay catálogo hijo al que navegar: `ActividadFormativa` no compone nada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirActividadFormativaView`

**Responsabilidades:**
- presenta los datos de la `ActividadFormativa`: `codigo` y `nombre`.
- permite solicitar editar o volver al listado.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` -- el `Admin` abre una `ActividadFormativa` del listado.
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
- porta `codigo` y `nombre`.

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- recupera la `ActividadFormativa` por identificador (`obtener(actividadFormativaId)`).

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/wireframes.puml) -- fuente de verdad de el detalle de solo lectura..
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : abrirActividadFormativa()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo de `Universidad` (`Universidad *-- ActividadFormativa`).
- [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md) -- clúster plantilla.
- [`abrirActividadesFormativas()`](../abrirActividadesFormativas/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarActividadFormativa()`](../editarActividadFormativa/README.md) -- edición disponible desde el detalle.
