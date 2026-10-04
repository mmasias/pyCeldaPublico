<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignaturas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado completo de `Asignatura` -- catálogo institucional plano que cuelga directamente de `SISTEMA_DISPONIBLE` (sin composición padre, a diferencia de `Facultad` bajo `Universidad`), reutilizado por `AsignaturaPrograma` en cada `Programa`. Cada fila muestra `nombre`, `ects` y `estado` (Vigente/Extinguido).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignaturas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturasView`

**Responsabilidades:**
- presenta el listado de `Asignatura`: `nombre`, `ects`, `estado`.
- ofrece la navegación a abrir cada `Asignatura` y a crear una nueva (`[+ Crear Asignatura]`).

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir Asignaturas.
- **Control:** `AsignaturaController`.
- **Salida:** `:ASIGNATURAS_ABIERTO`.

## Clases de controlador

### `AsignaturaController`

**Responsabilidades:**
- lista las `Asignatura` del catálogo (`listarAsignaturas()`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturasView`.
- **Salida:** `AsignaturaRepository`.

## Clases de modelo

### `Asignatura`

**Responsabilidades:**
- porta `codigo`, `nombre`, `ects`, `contenido` y `estado` (Vigente/Extinguido) -- `nombre`, `ects` y `estado` son los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- lista las `Asignatura` (`listar()`).

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** gestiona `Asignatura`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> ASIGNATURAS_ABIERTO : abrirAsignaturas()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (nombre, ects, contenido, estado), catálogo independiente reutilizado por `AsignaturaPrograma`.
- [`abrirAsignatura()`](../abrirAsignatura/README.md) / [`crearAsignatura()`](../crearAsignatura/README.md) / [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirUniversidades()`](../abrirUniversidades/README.md) -- mismo patrón de listado plano sin composición padre, mismo `SISTEMA_DISPONIBLE` de entrada.
