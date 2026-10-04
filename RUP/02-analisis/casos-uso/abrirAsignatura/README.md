<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta los datos de la `Asignatura` (`nombre`, `ects`, `estado`, `contenido`) y ofrece editar o volver al listado. `Asignatura` no tiene composición debajo -- a diferencia de `Universidad`/`Facultad`, desde aquí no se navega a ningún catálogo hijo, solo a la edición del propio detalle.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignatura/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturaView`

**Responsabilidades:**
- presenta el `nombre`, los `ects`, el `estado` y el `contenido` de la `Asignatura`.
- ofrece la navegación a editar y a volver al listado (`[Editar]`/`[Volver al listado]`).

**Colaboraciones:**
- **Entrada:** `:ASIGNATURAS_ABIERTO` -- el `Admin` solicita abrir una `Asignatura` del listado.
- **Control:** `AsignaturaController`.
- **Salida:** `:ASIGNATURA_ABIERTO`.

## Clases de controlador

### `AsignaturaController`

**Responsabilidades:**
- recupera la `Asignatura` (`cargarAsignatura(asignaturaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturaView`.
- **Salida:** `AsignaturaRepository`.

## Clases de modelo

### `Asignatura`

**Responsabilidades:**
- porta `codigo`, `nombre`, `ects`, `contenido` y `estado` (Vigente/Extinguido) -- los datos mostrados en el detalle.

**Colaboraciones:**
- **Entrada:** recuperada por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- recupera la `Asignatura` por identificador (`obtener(asignaturaId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** gestiona `Asignatura`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURAS_ABIERTO --> ASIGNATURA_ABIERTO : abrirAsignatura()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (nombre, ects, contenido, estado).
- [`abrirAsignaturas()`](../abrirAsignaturas/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarAsignatura()`](../editarAsignatura/README.md) -- destino del botón `[Editar]`.
- [`abrirUniversidad()`](../abrirUniversidad/README.md) -- mismo patrón de detalle de solo lectura.
