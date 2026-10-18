<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadesFormativas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirActividadesFormativas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirActividadesFormativas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): un solo paso, de solo lectura. Presenta el catálogo de `ActividadFormativa` de un `Programa`, con entrada desde `:PROGRAMA_ABIERTO`, mismo patrón que [`abrirCompetencias()`](../abrirCompetencias/README.md). Sin `<<choice>>`: la salida es única a `:ACTIVIDADES_FORMATIVAS_ABIERTO`. `Admin` y `DirectorPrograma` comparten la colaboración; la diferencia de alcance (cualquier `Programa` o los que dirige) es de autorización, no de análisis.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirActividadesFormativas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirActividadesFormativasView`

**Responsabilidades:**
- presenta el catálogo de `ActividadFormativa` del `Programa`, con `nombre` y `codigo` por fila, en orden de alta.
- permite abrir, crear o eliminar una `ActividadFormativa` desde el listado.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el actor abre la pestaña de actividades formativas del programa.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDADES_FORMATIVAS_ABIERTO`.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- obtiene el catálogo del `Programa` (`listarActividadesFormativasDelPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `AbrirActividadesFormativasView`.
- **Salida:** `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- porta `codigo` y `nombre` -- los datos presentados por fila.

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- lista las `ActividadFormativa` del `Programa` (`listarDelPrograma(programaId)`), en orden de alta.

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/wireframes.puml) -- fuente de verdad del listado y la salida única.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo del `Programa` (`Programa *-- ActividadFormativa`). Hasta #772, catálogo de `Universidad` (issue [#655](https://github.com/mmasias/pyCelda/issues/655)).
- [`abrirCompetencias()`](../abrirCompetencias/README.md) -- patrón de origen.
- [`abrirActividadFormativa()`](../abrirActividadFormativa/README.md) -- destino de navegación del listado.
