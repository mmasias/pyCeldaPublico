<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirFacultades()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirFacultades/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirFacultades()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de `Facultad` de una `Universidad` concreta -- `Facultad` no es catálogo plano sino composición real (`Universidad *-d- Facultad`), se navega desde dentro de la `Universidad`, mismo criterio que `Programa` dentro de `Facultad`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirFacultades/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirFacultadesView`

**Responsabilidades:**
- presenta el listado de `Facultad` de la `Universidad` abierta: `nombre`.
- ofrece la navegación a abrir cada `Facultad` y a eliminarla (`[Abrir]`/`[Eliminar]` por fila), y a crear una nueva (`[+ Crear Facultad]`).

**Colaboraciones:**
- **Entrada:** `:UNIVERSIDAD_ABIERTO` -- el `Admin` solicita abrir las Facultades de la `Universidad` abierta.
- **Control:** `FacultadController`.
- **Salida:** `:FACULTADES_ABIERTO`.

## Clases de controlador

### `FacultadController`

**Responsabilidades:**
- lista las `Facultad` de una `Universidad` (`listarFacultadesDeLaUniversidad(universidadId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirFacultadesView`.
- **Salida:** `FacultadRepository`.

## Clases de modelo

### `Facultad`

**Responsabilidades:**
- porta `nombre` -- el único atributo real de la entidad, el dato mostrado en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `FacultadRepository`.

### `FacultadRepository`

**Responsabilidades:**
- lista las `Facultad` de una `Universidad` (`listarDeLaUniversidad(universidadId)`).

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** gestiona `Facultad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDAD_ABIERTO --> FACULTADES_ABIERTO : abrirFacultades()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad *-d- Facultad`, `Facultad *-d- Programa`.
- [`abrirFacultad()`](../abrirFacultad/README.md) / [`crearFacultad()`](../crearFacultad/README.md) / [`eliminarFacultad()`](../eliminarFacultad/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirUniversidad()`](../abrirUniversidad/README.md) -- quien abre la `Universidad` desde la que se navega.
