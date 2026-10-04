<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearPrograma/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/README.md): CRUD real e inmediato contra `ProgramaRepository`. A diferencia de [`crearUniversidad()`](../crearUniversidad/README.md) (un solo campo obligatorio), aquí el formulario pide `codigo` y `nombre` a la vez, ambos obligatorios -- no hay nada que deferir a la edición, `editarPrograma()` no completa ningún campo adicional (el `codigo` ya no es editable tras la creación). Diferencia real frente a [`crearAsignatura()`](../crearAsignatura/README.md) (que desde el issue #181 también exige `codigo`+`nombre`, pero sigue deferiendo `ects`/`contenido` a `editarAsignatura()`): aquí no queda nada por completar después. `estado` nace `Vigente` por defecto, sin pedirlo. Es la primera escritura de `Admin` sobre `Programa`: hasta ahora el alta de catálogo institucional era por SQL en bloque (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)); esta rebanada construye la escritura que faltaba, apoyándose en el listado Admin de [`abrirProgramas()`](../abrirProgramas/README.md) como punto de entrada.

**Retocado (issue #148, 2026-09-05)**: `<<choice>>` de rechazo por `codigo` duplicado, mismo patrón que [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) (máximo superado) -- antes la salida era única.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearProgramaView`

**Responsabilidades:**
- presenta el formulario de creación: `codigo` y `nombre`, ambos obligatorios.
- presenta el aviso de rechazo cuando el `<<choice>>` sale rojo.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:PROGRAMAS_ABIERTO` -- el `Admin` solicita crear un `Programa` desde el listado.
- **Control:** `ProgramaController`.
- **Salida:** `:Collaboration EditarPrograma` vía `<<include>> editarPrograma()` (verde) o `:PROGRAMAS_ABIERTO` sin crear (rojo, código ya existente).

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- valida que `codigo` y `nombre` estén presentes (`validarDatosObligatorios(codigo, nombre)`).
- aplica el `<<choice>>` de unicidad: comprueba si el `codigo` ya existe (`ProgramaRepository.existeCodigo(codigo)`) antes de crear -- dentro -> crea; ya existente -> no crea nada.
- crea el `Programa` directamente en `ProgramaRepository`, real e inmediato (`crearPrograma(codigo, nombre)`).

**Colaboraciones:**
- **Entrada:** `CrearProgramaView`.
- **Salida:** `ProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- porta `codigo` y `nombre` desde el momento de crearse; `estado` nace `Vigente` sin pedirlo.

**Colaboraciones:**
- **Entrada:** creada por `ProgramaRepository`.

### `ProgramaRepository`

**Responsabilidades:**
- comprueba si ya existe un `Programa` con ese `codigo` (`existeCodigo(codigo)`) -- global al catálogo, no por `Facultad`.
- crea el `Programa` (`crear(codigo, nombre)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/wireframes.puml) -- fuente de verdad del formulario (`codigo`+`nombre` obligatorios), salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : crearPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa` (codigo, estado); "nada del catálogo se borra físicamente", `estado` Vigente/Extinguido.
- [`editarPrograma()`](../editarPrograma/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.
- [`crearAsignatura()`](../crearAsignatura/README.md) -- mismo patrón de creación con `<<choice>>` de rechazo por código duplicado (desde el issue #181), pero sigue deferiendo `ects`/`contenido` al `<<include>>` de salida.
- [`abrirProgramas()`](../abrirProgramas/README.md) -- listado que sirve de punto de entrada; su variante `Admin` se construye en Diseño junto a este caso de uso.
