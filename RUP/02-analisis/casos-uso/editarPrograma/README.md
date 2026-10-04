<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPrograma/README.md): CRUD real e inmediato contra `ProgramaRepository`. Sin `<<choice>>` -- `Programa` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo los obligatorios `codigo` y `nombre`. Diferencia real frente a [`editarAsignatura()`](../editarAsignatura/README.md)/[`editarUniversidad()`](../editarUniversidad/README.md): el único campo editable es `nombre` -- `codigo` se muestra pero no es editable tras la creación (el wireframe lo deja explícito: "El código no es editable una vez creado el Programa"), porque el `codigo` es un identificador real usado fuera del propio nombre (URLs, nomenclatura de ficheros del corpus, discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)). `estado` queda fuera del formulario: se gestiona en exclusiva desde [`eliminarPrograma()`](../eliminarPrograma/README.md) (Vigente/Extinguido). `Programa` gana aquí su método `actualizar(nombre)`, mismo patrón que `Universidad.actualizar(nombre)`. Es también el destino del `<<include>>` de [`crearPrograma()`](../crearPrograma/README.md): tras crear, el `Admin` queda editando el `Programa` recién creado.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarProgramaView`

**Responsabilidades:**
- presenta el formulario con los datos actuales del `Programa`: `codigo` mostrado como solo lectura, `nombre` editable -- sin `estado`.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `Admin` solicita editar el `Programa` abierto; también alcanzado como `<<include>>` de `crearPrograma()`.
- **Control:** `ProgramaController`.
- **Salida:** `:PROGRAMA_ABIERTO`.

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- recupera el `Programa` a editar (`cargarPrograma(programaId)`, mismo método introducido por [`abrirPrograma()`](../abrirPrograma/README.md)).
- valida los obligatorios (`validarDatosObligatorios(codigo, nombre)` -- el mismo método ya usado en crear; Análisis no distingue firmas por fase, mismo criterio que `AsignaturaController`).
- guarda los cambios (`guardarCambios(programaId, nombre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente al `Programa` que se actualice y persiste. Solo `nombre` viaja: el `codigo` no se puede mutar aquí.

**Colaboraciones:**
- **Entrada:** `EditarProgramaView`.
- **Salida:** `Programa`, `ProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- porta `codigo` y `nombre`; solo `nombre` es editable.
- se actualiza a sí misma (`actualizar(nombre)`) -- mismo patrón que `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** persistida por `ProgramaRepository`.

### `ProgramaRepository`

**Responsabilidades:**
- recupera el `Programa` por identificador (`obtener(programaId)`).
- persiste la actualización (`actualizar(programa)`).

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarPrograma/wireframes.puml) -- fuente de verdad del formulario (`codigo` solo lectura, `nombre` editable), sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : editarPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa` (codigo, estado); `codigo` con peso en la integridad del catálogo (#18); `estado` fuera del formulario.
- [`crearPrograma()`](../crearPrograma/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí.
- [`abrirPrograma()`](../abrirPrograma/README.md) -- mismo `ProgramaController.cargarPrograma(programaId)`, reutilizado.
- [`eliminarPrograma()`](../eliminarPrograma/README.md) -- único gestor del `estado`, fuera de este formulario.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
