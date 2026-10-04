<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadesFormativas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirActividadesFormativas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirActividadesFormativas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md): un solo paso, de solo lectura. Presenta el listado de `ActividadFormativa` de una `Universidad` -- catálogo que cuelga directamente de `:SISTEMA_DISPONIBLE` (entrada desde `abrirPanelAdministracion()`, sin composición padre propia). Sin `<<choice>>`: la salida es única a `:ACTIVIDADES_FORMATIVAS_ABIERTO`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirActividadesFormativas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirActividadesFormativasView`

**Responsabilidades:**
- presenta el listado de `ActividadFormativa` de la `Universidad` elegida, con `codigo` y `nombre` por fila.
- permite abrir, crear o eliminar una `ActividadFormativa` desde el listado.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir las actividades formativas.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDADES_FORMATIVAS_ABIERTO`.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- obtiene el listado de la `Universidad` (`listarActividadesFormativas(universidadId)`).

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
- lista las `ActividadFormativa` de la `Universidad` (`listarDeLaUniversidad(universidadId)`), orden de alta.

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/wireframes.puml) -- fuente de verdad de el listado y la salida única..
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> ACTIVIDADES_FORMATIVAS_ABIERTO : abrirActividadesFormativas()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo de `Universidad` (`Universidad *-- ActividadFormativa`).
- [`abrirMetodologiasDocentes()`](../abrirMetodologiasDocentes/README.md) -- clúster plantilla, mismo patrón de listado de catálogo.
- [`abrirActividadFormativa()`](../abrirActividadFormativa/README.md) -- destino de navegación del listado.
