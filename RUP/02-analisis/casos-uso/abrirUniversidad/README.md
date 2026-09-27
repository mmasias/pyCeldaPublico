<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirUniversidad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirUniversidad()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta los datos de la `Universidad` (`nombre`) y ofrece editar, volver al listado o navegar a las `Facultad` que la componen -- es el estado desde el que se alcanza [`abrirFacultades()`](../abrirFacultades/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirUniversidad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirUniversidadView`

**Responsabilidades:**
- presenta el `nombre` de la `Universidad`.
- ofrece la navegación a editar, a volver al listado y a las `Facultad` que la componen (`[Editar]`/`[Ver Facultades]`/`[Volver al listado]`).

**Colaboraciones:**
- **Entrada:** `:UNIVERSIDADES_ABIERTO` -- el `Admin` solicita abrir una `Universidad` del listado.
- **Control:** `UniversidadController`.
- **Salida:** `:UNIVERSIDAD_ABIERTO`.

## Clases de controlador

### `UniversidadController`

**Responsabilidades:**
- recupera la `Universidad` (`cargarUniversidad(universidadId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirUniversidadView`.
- **Salida:** `UniversidadRepository`.

## Clases de modelo

### `Universidad`

**Responsabilidades:**
- porta `nombre` -- el único atributo real de la entidad, el dato mostrado.

**Colaboraciones:**
- **Entrada:** recuperada por `UniversidadRepository`.

### `UniversidadRepository`

**Responsabilidades:**
- recupera la `Universidad` por identificador (`obtener(universidadId)`).

**Colaboraciones:**
- **Entrada:** `UniversidadController`.
- **Salida:** gestiona `Universidad`.

## Hallazgo: hueco en el wireframe de Requisitos (corregido)

El diagrama de contexto de `Admin` declara `UNIVERSIDAD_ABIERTO --> FACULTADES_ABIERTO : abrirFacultades()`, pero el wireframe de este caso de uso solo ofrecía `[Editar]`/`[Volver al listado]` -- faltaba el punto de entrada visual a ese camino. Confirmado por Manuel: se corrigió en Requisitos antes de continuar con este Análisis, añadiendo `[Ver Facultades]` al wireframe ([wireframes.puml](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/wireframes.puml)) y regenerando su SVG. Mismo hueco encontrado en paralelo en [`abrirFacultad()`](../abrirFacultad/README.md) (falta de botón hacia `abrirGrados()`), también corregido.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/wireframes.puml) -- fuente de verdad del contenido presentado, ya con el botón `[Ver Facultades]` (ver hallazgo arriba).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDADES_ABIERTO --> UNIVERSIDAD_ABIERTO : abrirUniversidad()`, `UNIVERSIDAD_ABIERTO --> FACULTADES_ABIERTO : abrirFacultades()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`, `Universidad *-d- Facultad`.
- [`abrirUniversidades()`](../abrirUniversidades/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- destino del botón `[Editar]`.
- [`abrirFacultades()`](../abrirFacultades/README.md) -- destino del botón `[Ver Facultades]`.
