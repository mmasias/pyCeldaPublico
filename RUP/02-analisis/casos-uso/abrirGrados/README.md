<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirGrados()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirGrados/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirGrados()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/README.md), en su variante invocada por `DirectorGrado`: un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de `Grado` que dirige, sin las acciones de alta/baja/eliminación que sí ofrece la variante de `Admin` (fuera de alcance de esta rebanada, ver más abajo).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirGrados/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirGradosView`

**Responsabilidades:**
- presenta el listado de `Grado` que dirige el `DirectorGrado`: `codigo`, `nombre`, `estado`.
- ofrece la navegación a abrir cada `Grado`.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `DirectorGrado` solicita volver al listado de sus Grados. También `<<include>>` de [`abrirInicio()`](../abrirInicio/README.md) como sección "Mis grados" (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274); antes extendía a `iniciarSesion()` directamente), fuera de alcance de este diagrama -- ver Simplificación más abajo.
- **Control:** `GradoController`.
- **Salida:** `:GRADOS_ABIERTO`.

## Clases de controlador

### `GradoController`

**Responsabilidades:**
- lista los `Grado` que dirige un `DirectorGrado` (`listarPropios(directorGradoId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirGradosView`.
- **Salida:** `GradoRepository`.

## Clases de modelo

### `Grado`

**Responsabilidades:**
- porta `codigo` y `estado` -- los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listado por `GradoRepository`.

### `GradoRepository`

**Responsabilidades:**
- lista los `Grado` dirigidos por un `DirectorGrado` (`listarDirigidosPor(directorGradoId)`) -- `Grado o- DirectorGrado`, agregación sin exclusividad (un director puede dirigir varios Grados).

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `Grado`.

## Simplificación fuera de alcance de esta rebanada

**Variante de `Admin`**: la especificación de Requisitos es compartida -- `Admin` invoca `abrirGrados()` sin filtro, con acciones `[Eliminar]`/`+ Crear Grado`, sobre el listado completo de una `Facultad`. Esta rebanada cubre exclusivamente el camino de `DirectorGrado` (filtrado a sus propios Grados, sin esas acciones), mismo criterio que [`abrirGuia()`](../abrirGuia/README.md) cubrió solo el camino de `Profesor` en su momento. `crearGrado()`/`editarGrado()`/`eliminarGrado()` son de `Admin`, fuera de alcance de esta rebanada (decisión de la discussion [#65](https://github.com/mmasias/pyCelda/discussions/65): el alta de catálogo institucional es por SQL en bloque, no por interfaz).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/wireframes.puml) -- fuente de verdad, incluida la variante `wireframe-porDirector`.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> GRADOS_ABIERTO : abrirGrados()`, `INICIO_ABIERTO --> GRADOS_ABIERTO : abrirGrados()`; el aterrizaje tras el login es `INICIO_ABIERTO` (`iniciarSesion()`).
- [`abrirInicio()`](../abrirInicio/README.md) -- primitiva que incluye esta variante como sección "Mis grados".
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado{codigo, estado}`, `Grado o- DirectorGrado`.
- [`abrirGrado()`](../abrirGrado/README.md) -- caso de uso alcanzado desde cada fila de este listado.
