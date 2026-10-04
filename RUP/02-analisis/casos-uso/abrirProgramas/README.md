<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProgramas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirProgramas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirProgramas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/README.md), en su variante invocada por `DirectorPrograma`: un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de `Programa` que dirige, sin las acciones de alta/baja/eliminación que sí ofrece la variante de `Admin` (fuera de alcance de esta rebanada, ver más abajo).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirProgramas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirProgramasView`

**Responsabilidades:**
- presenta el listado de `Programa` que dirige el `DirectorPrograma`: `codigo`, `nombre`, `estado`.
- ofrece la navegación a abrir cada `Programa`.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita volver al listado de sus Programas. También `<<include>>` de [`abrirInicio()`](../abrirInicio/README.md) como sección "Mis programas" (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274); antes extendía a `iniciarSesion()` directamente), fuera de alcance de este diagrama -- ver Simplificación más abajo.
- **Control:** `ProgramaController`.
- **Salida:** `:PROGRAMAS_ABIERTO`.

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- lista los `Programa` que dirige un `DirectorPrograma` (`listarPropios(directorProgramaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirProgramasView`.
- **Salida:** `ProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- porta `codigo` y `estado` -- los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listado por `ProgramaRepository`.

### `ProgramaRepository`

**Responsabilidades:**
- lista los `Programa` dirigidos por un `DirectorPrograma` (`listarDirigidosPor(directorProgramaId)`) -- `Programa o- DirectorPrograma`, agregación sin exclusividad (un director puede dirigir varios Programas).

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

## Simplificación fuera de alcance de esta rebanada

**Variante de `Admin`**: la especificación de Requisitos es compartida -- `Admin` invoca `abrirProgramas()` sin filtro, con acciones `[Eliminar]`/`+ Crear Programa`, sobre el listado completo de una `Facultad`. Esta rebanada cubre exclusivamente el camino de `DirectorPrograma` (filtrado a sus propios Programas, sin esas acciones), mismo criterio que [`abrirGuia()`](../abrirGuia/README.md) cubrió solo el camino de `Profesor` en su momento. `crearPrograma()`/`editarPrograma()`/`eliminarPrograma()` son de `Admin`, fuera de alcance de esta rebanada (decisión de la discussion [#65](https://github.com/mmasias/pyCelda/discussions/65): el alta de catálogo institucional es por SQL en bloque, no por interfaz).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/wireframes.puml) -- fuente de verdad, incluida la variante `wireframe-porDirector`.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()`, `INICIO_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()`; el aterrizaje tras el login es `INICIO_ABIERTO` (`iniciarSesion()`).
- [`abrirInicio()`](../abrirInicio/README.md) -- primitiva que incluye esta variante como sección "Mis programas".
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa{codigo, estado}`, `Programa o- DirectorPrograma`.
- [`abrirPrograma()`](../abrirPrograma/README.md) -- caso de uso alcanzado desde cada fila de este listado.
