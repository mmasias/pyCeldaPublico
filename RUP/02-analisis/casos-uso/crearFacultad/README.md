<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearFacultad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearFacultad()`](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/README.md): CRUD real e inmediato contra `FacultadRepository`. La fila se crea con `universidadId` desde el principio -- pertenece a su `Universidad` desde el momento de crearse (`Universidad *-d- Facultad`, composición, no catálogo plano). Un único campo obligatorio (`nombre`) y sin `<<choice>>`. La salida es única, sin rama de rechazo: `<<include>> editarFacultad()`, mismo patrón que [`crearUniversidad()`](../crearUniversidad/README.md) -- la transición de salida lleva la nota `editarFacultad()` (regla de Requisitos).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearFacultad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearFacultadView`

**Responsabilidades:**
- presenta el formulario de creación: `nombre`, obligatorio.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:FACULTADES_ABIERTO` -- el `Admin` solicita crear una `Facultad` para la `Universidad` abierta.
- **Control:** `FacultadController`.
- **Salida:** `:Collaboration EditarFacultad` vía `<<include>> editarFacultad()`.

## Clases de controlador

### `FacultadController`

**Responsabilidades:**
- valida que `nombre` esté presente (`validarDatosObligatorios(nombre)`).
- crea la `Facultad` en la `Universidad` abierta, directamente en `FacultadRepository`, real e inmediato (`crearFacultad(universidadId, nombre)`).

**Colaboraciones:**
- **Entrada:** `CrearFacultadView`.
- **Salida:** `FacultadRepository`.

## Clases de modelo

### `Facultad`

**Responsabilidades:**
- porta `nombre` y su enlace a la `Universidad` (`universidadId`) desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `FacultadRepository`.

### `FacultadRepository`

**Responsabilidades:**
- crea la `Facultad` dentro de una `Universidad` (`crear(universidadId, nombre)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** gestiona `Facultad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/wireframes.puml) -- fuente de verdad del formulario, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTADES_ABIERTO --> FACULTAD_ABIERTO : crearFacultad()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad *-d- Facultad`.
- [`editarFacultad()`](../editarFacultad/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.
- [`crearUniversidad()`](../crearUniversidad/README.md) -- mismo patrón de creación con salida única vía `<<include>>`, un nivel arriba.
