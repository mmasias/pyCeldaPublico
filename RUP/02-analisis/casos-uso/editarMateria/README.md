<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/README.md): CRUD real e inmediato contra `MateriaRepository`. Sin `<<choice>>` -- `Materia` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, y su único atributo editable es `nombre` (toda su otra información es la relación de composición con `Programa`, que no se muta aquí: cambiar el reparto de una `Materia` de un `Programa` implica un `Programa` nuevo, no una edición del existente). Mismo patrón exacto que [`editarPrograma()`](../editarPrograma/README.md) y [`editarFacultad()`](../editarFacultad/README.md): formulario nombre-only, `actualizar(nombre)` como único método del modelo. `Materia` gana aquí su método `actualizar(nombre)`. Es también el destino del `<<include>>` de [`crearMateria()`](../crearMateria/README.md): tras crear, el `Admin` queda editando la `Materia` recién creada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarMateriaView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la `Materia`: `nombre` editable.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `Admin` solicita editar la `Materia` abierta; también alcanzado como `<<include>>` de `crearMateria()`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera la `Materia` a editar (`cargarMateria(materiaId)`, mismo método introducido por la variante Admin de [`abrirMateria()`](../abrirMateria/README.md)).
- valida el obligatorio (`validarDatosObligatorios(nombre)` -- el mismo método ya usado en crear; Análisis no distingue firmas por fase, mismo criterio que `ProgramaController`).
- guarda los cambios (`guardarCambios(materiaId, nombre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente a la `Materia` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarMateriaView`.
- **Salida:** `Materia`, `MateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre`; único atributo editable.
- se actualiza a sí misma (`actualizar(nombre)`) -- mismo patrón que `Programa.actualizar(nombre)` y `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** persistida por `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` por identificador (`obtener(materiaId)`).
- persiste la actualización (`actualizar(materia)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarMateria/wireframes.puml) -- fuente de verdad del formulario nombre-only, sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia{nombre}`; sin `estado` propio.
- [`crearMateria()`](../crearMateria/README.md) -- `<<include>>` de origen, cerrado en este mismo lote apuntando aquí.
- [`abrirMateria()`](../abrirMateria/README.md) -- mismo `MateriaController.cargarMateria(materiaId)`, reutilizado.
- [`editarPrograma()`](../editarPrograma/README.md) / [`editarFacultad()`](../editarFacultad/README.md) -- mismo patrón de edición nombre-only sin `<<choice>>` de negocio.
