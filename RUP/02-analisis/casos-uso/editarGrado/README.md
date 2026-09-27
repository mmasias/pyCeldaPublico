<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/README.md): CRUD real e inmediato contra `GradoRepository`. Sin `<<choice>>` -- `Grado` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo los obligatorios `codigo` y `nombre`. Diferencia real frente a [`editarAsignatura()`](../editarAsignatura/README.md)/[`editarUniversidad()`](../editarUniversidad/README.md): el único campo editable es `nombre` -- `codigo` se muestra pero no es editable tras la creación (el wireframe lo deja explícito: "El código no es editable una vez creado el Grado"), porque el `codigo` es un identificador real usado fuera del propio nombre (URLs, nomenclatura de ficheros del corpus, discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)). `estado` queda fuera del formulario: se gestiona en exclusiva desde [`eliminarGrado()`](../eliminarGrado/README.md) (Vigente/Extinguido). `Grado` gana aquí su método `actualizar(nombre)`, mismo patrón que `Universidad.actualizar(nombre)`. Es también el destino del `<<include>>` de [`crearGrado()`](../crearGrado/README.md): tras crear, el `Admin` queda editando el `Grado` recién creado.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarGradoView`

**Responsabilidades:**
- presenta el formulario con los datos actuales del `Grado`: `codigo` mostrado como solo lectura, `nombre` editable -- sin `estado`.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `Admin` solicita editar el `Grado` abierto; también alcanzado como `<<include>>` de `crearGrado()`.
- **Control:** `GradoController`.
- **Salida:** `:GRADO_ABIERTO`.

## Clases de controlador

### `GradoController`

**Responsabilidades:**
- recupera el `Grado` a editar (`cargarGrado(gradoId)`, mismo método introducido por [`abrirGrado()`](../abrirGrado/README.md)).
- valida los obligatorios (`validarDatosObligatorios(codigo, nombre)` -- el mismo método ya usado en crear; Análisis no distingue firmas por fase, mismo criterio que `AsignaturaController`).
- guarda los cambios (`guardarCambios(gradoId, nombre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente al `Grado` que se actualice y persiste. Solo `nombre` viaja: el `codigo` no se puede mutar aquí.

**Colaboraciones:**
- **Entrada:** `EditarGradoView`.
- **Salida:** `Grado`, `GradoRepository`.

## Clases de modelo

### `Grado`

**Responsabilidades:**
- porta `codigo` y `nombre`; solo `nombre` es editable.
- se actualiza a sí misma (`actualizar(nombre)`) -- mismo patrón que `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** persistida por `GradoRepository`.

### `GradoRepository`

**Responsabilidades:**
- recupera el `Grado` por identificador (`obtener(gradoId)`).
- persiste la actualización (`actualizar(grado)`).

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `Grado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/wireframes.puml) -- fuente de verdad del formulario (`codigo` solo lectura, `nombre` editable), sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GRADO_ABIERTO : editarGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado` (codigo, estado); `codigo` con peso en la integridad del catálogo (#18); `estado` fuera del formulario.
- [`crearGrado()`](../crearGrado/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí.
- [`abrirGrado()`](../abrirGrado/README.md) -- mismo `GradoController.cargarGrado(gradoId)`, reutilizado.
- [`eliminarGrado()`](../eliminarGrado/README.md) -- único gestor del `estado`, fuera de este formulario.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
