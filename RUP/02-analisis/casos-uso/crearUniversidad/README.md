<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearUniversidad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearUniversidad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearUniversidad()`](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/README.md): CRUD real e inmediato contra `UniversidadRepository`. Un único campo obligatorio (`nombre`) y sin `<<choice>>` -- `Universidad` no tiene ninguna regla de negocio documentada en el modelo de dominio. La salida es única, sin rama de rechazo: `<<include>> editarUniversidad()`, mismo patrón que [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- la transición de salida lleva la nota `editarUniversidad()` (regla de Requisitos).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearUniversidad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearUniversidadView`

**Responsabilidades:**
- presenta el formulario de creación: `nombre`, obligatorio.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:UNIVERSIDADES_ABIERTO` -- el `Admin` solicita crear una `Universidad` desde el listado.
- **Control:** `UniversidadController`.
- **Salida:** `:Collaboration EditarUniversidad` vía `<<include>> editarUniversidad()`.

## Clases de controlador

### `UniversidadController`

**Responsabilidades:**
- valida que `nombre` esté presente (`validarDatosObligatorios(nombre)`).
- crea la `Universidad` directamente en `UniversidadRepository`, real e inmediato (`crearUniversidad(nombre)`).

**Colaboraciones:**
- **Entrada:** `CrearUniversidadView`.
- **Salida:** `UniversidadRepository`.

## Clases de modelo

### `Universidad`

**Responsabilidades:**
- porta `nombre` desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `UniversidadRepository`.

### `UniversidadRepository`

**Responsabilidades:**
- crea la `Universidad` (`crear(nombre)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `UniversidadController`.
- **Salida:** gestiona `Universidad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/wireframes.puml) -- fuente de verdad del formulario, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDADES_ABIERTO --> UNIVERSIDAD_ABIERTO : crearUniversidad()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.
- [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- mismo patrón de creación con salida única vía `<<include>>`.
