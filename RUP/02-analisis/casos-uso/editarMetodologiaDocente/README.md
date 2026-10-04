<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md): CRUD real e inmediato contra `MetodologiaDocenteRepository`. Sin `<<choice>>` -- `MetodologiaDocente` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo los obligatorios `codigo` y `descripcion`. Regla de Requisitos: el `codigo` no es editable una vez creada la metodología -- el formulario lo muestra de solo lectura y la edición reenvía su valor sin cambios. `MetodologiaDocente` gana aquí su método `actualizar(codigo, descripcion)`, mismo patrón que `Asignatura.actualizar(nombre, ects, contenido)`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarMetodologiaDocenteView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la `MetodologiaDocente` (`codigo`, `descripcion`) -- el `codigo` de solo lectura, regla de Requisitos.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIA_DOCENTE_ABIERTO` -- el `Admin` solicita editar la `MetodologiaDocente` abierta; también es el destino del alta de [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md).
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIA_DOCENTE_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- recupera la `MetodologiaDocente` a editar (`cargarMetodologiaDocente(metodologiaDocenteId)`, mismo método introducido por [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md)).
- valida los obligatorios (`validarDatosObligatorios(codigo, descripcion)` -- el mismo método ya usado en crear; Análisis no distingue firmas por fase, mismo criterio que `AsignaturaController`).
- guarda los cambios (`guardarCambios(metodologiaDocenteId, codigo, descripcion)`): sin `<<choice>>` de negocio que aplicar -- pide directamente a la `MetodologiaDocente` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocente`, `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion`.
- se actualiza a sí misma (`actualizar(codigo, descripcion)`) -- mismo patrón que `Asignatura.actualizar(nombre, ects, contenido)`.

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** persistida por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- recupera la `MetodologiaDocente` por identificador (`obtener(metodologiaDocenteId)`).
- persiste la actualización (`editar(metodologiaDocente)`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo y con el `codigo` no editable.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIA_DOCENTE_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : editarMetodologiaDocente()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente { codigo, descripcion }`.
- [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md) -- el alta alcanza el detalle desde el que se edita, sin `<<include>>` C->U.
- [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md) -- mismo `MetodologiaDocenteController.cargarMetodologiaDocente(metodologiaDocenteId)`, reutilizado.
- [`eliminarMetodologiaDocente()`](../eliminarMetodologiaDocente/README.md) -- el otro caso de uso que muta el catálogo, con `<<choice>>` bloqueante.
- [`editarAsignatura()`](../editarAsignatura/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
