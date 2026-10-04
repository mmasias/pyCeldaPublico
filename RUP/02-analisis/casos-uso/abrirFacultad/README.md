<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirFacultad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirFacultad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirFacultad()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta los datos de la `Facultad` (`nombre`) y ofrece editar, volver al listado o navegar a los `Programa` que la componen -- es el estado desde el que se alcanza [`abrirProgramas()`](../abrirProgramas/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirFacultad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirFacultadView`

**Responsabilidades:**
- presenta el `nombre` de la `Facultad`.
- ofrece la navegación a editar, a volver al listado y a los `Programa` que la componen (`[Editar]`/`[Ver Programas]`/`[Volver al listado]`).

**Colaboraciones:**
- **Entrada:** `:FACULTADES_ABIERTO` -- el `Admin` solicita abrir una `Facultad` del listado.
- **Control:** `FacultadController`.
- **Salida:** `:FACULTAD_ABIERTO`.

## Clases de controlador

### `FacultadController`

**Responsabilidades:**
- recupera la `Facultad` (`cargarFacultad(facultadId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirFacultadView`.
- **Salida:** `FacultadRepository`.

## Clases de modelo

### `Facultad`

**Responsabilidades:**
- porta `nombre` -- el único atributo real de la entidad, el dato mostrado.

**Colaboraciones:**
- **Entrada:** recuperada por `FacultadRepository`.

### `FacultadRepository`

**Responsabilidades:**
- recupera la `Facultad` por identificador (`obtener(facultadId)`).

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** gestiona `Facultad`.

## Hallazgo: hueco en el wireframe de Requisitos (corregido)

El diagrama de contexto de `Admin` declara `FACULTAD_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()`, pero el wireframe de este caso de uso solo ofrecía `[Editar]`/`[Volver al listado]` -- faltaba el punto de entrada visual a ese camino. Mismo hueco que el detectado en paralelo en [`abrirUniversidad()`](../abrirUniversidad/README.md). Confirmado por Manuel: se corrigió en Requisitos antes de continuar con este Análisis, añadiendo `[Ver Programas]` al wireframe ([wireframes.puml](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/wireframes.puml)) y regenerando su SVG.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/wireframes.puml) -- fuente de verdad del contenido presentado, ya con el botón `[Ver Programas]` (ver hallazgo arriba).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTADES_ABIERTO --> FACULTAD_ABIERTO : abrirFacultad()`, `FACULTAD_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Facultad`, `Facultad *-d- Programa`.
- [`abrirFacultades()`](../abrirFacultades/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarFacultad()`](../editarFacultad/README.md) -- destino del botón `[Editar]`.
- [`abrirProgramas()`](../abrirProgramas/README.md) -- destino del botón `[Ver Programas]`.
