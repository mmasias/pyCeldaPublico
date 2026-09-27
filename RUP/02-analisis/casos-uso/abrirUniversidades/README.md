<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirUniversidades()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirUniversidades/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirUniversidades()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado completo de `Universidad` -- primer nivel de la estructura curricular (`Universidad *-d- Facultad`), punto de entrada del `Admin` a toda la gestión de catálogo que cuelga de ella.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirUniversidades/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirUniversidadesView`

**Responsabilidades:**
- presenta el listado de `Universidad`: `nombre`.
- ofrece la navegación a abrir cada `Universidad` y a crear una nueva (`[+ Crear Universidad]`).

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir Universidades.
- **Control:** `UniversidadController`.
- **Salida:** `:UNIVERSIDADES_ABIERTO`.

## Clases de controlador

### `UniversidadController`

**Responsabilidades:**
- lista las `Universidad` del catálogo (`listarUniversidades()`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirUniversidadesView`.
- **Salida:** `UniversidadRepository`.

## Clases de modelo

### `Universidad`

**Responsabilidades:**
- porta `nombre` -- el único atributo real de la entidad, el dato mostrado en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `UniversidadRepository`.

### `UniversidadRepository`

**Responsabilidades:**
- lista las `Universidad` (`listar()`).

**Colaboraciones:**
- **Entrada:** `UniversidadController`.
- **Salida:** gestiona `Universidad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> UNIVERSIDADES_ABIERTO : abrirUniversidades()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`, `Universidad *-d- Facultad`.
- [`abrirUniversidad()`](../abrirUniversidad/README.md) / [`crearUniversidad()`](../crearUniversidad/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirFacultades()`](../abrirFacultades/README.md) -- caso de uso hijo, alcanzado desde `:UNIVERSIDAD_ABIERTO`.
