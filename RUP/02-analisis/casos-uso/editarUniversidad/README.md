<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarUniversidad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarUniversidad()`](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/README.md): CRUD real e inmediato contra `UniversidadRepository`. Sin `<<choice>>` -- `Universidad` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo el obligatorio `nombre`. `Universidad` gana aquí su método `actualizar(nombre)`, mismo patrón que `ReferenciaBibliografica.actualizar(tipo, referencia)`. Es también el destino del `<<include>>` de [`crearUniversidad()`](../crearUniversidad/README.md): tras crear, el `Admin` queda editando la `Universidad` recién creada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarUniversidad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarUniversidadView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la `Universidad` (`nombre`).
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:UNIVERSIDAD_ABIERTO` -- el `Admin` solicita editar la `Universidad` abierta; también alcanzado como `<<include>>` de `crearUniversidad()`.
- **Control:** `UniversidadController`.
- **Salida:** `:UNIVERSIDAD_ABIERTO`.

## Clases de controlador

### `UniversidadController`

**Responsabilidades:**
- recupera la `Universidad` a editar (`cargarUniversidad(universidadId)`, mismo método introducido por [`abrirUniversidad()`](../abrirUniversidad/README.md)).
- valida el obligatorio (`validarDatosObligatorios(nombre)`).
- guarda los cambios (`guardarCambios(universidadId, nombre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente a la `Universidad` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarUniversidadView`.
- **Salida:** `Universidad`, `UniversidadRepository`.

## Clases de modelo

### `Universidad`

**Responsabilidades:**
- porta `nombre`, editable.
- se actualiza a sí misma (`actualizar(nombre)`) -- mismo patrón que `ReferenciaBibliografica.actualizar(tipo, referencia)`.

**Colaboraciones:**
- **Entrada:** `UniversidadController`.
- **Salida:** persistida por `UniversidadRepository`.

### `UniversidadRepository`

**Responsabilidades:**
- recupera la `Universidad` por identificador (`obtener(universidadId)`).
- persiste la actualización (`actualizar(universidad)`).

**Colaboraciones:**
- **Entrada:** `UniversidadController`.
- **Salida:** gestiona `Universidad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarUniversidad/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDAD_ABIERTO --> UNIVERSIDAD_ABIERTO : editarUniversidad()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`.
- [`crearUniversidad()`](../crearUniversidad/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí.
- [`abrirUniversidad()`](../abrirUniversidad/README.md) -- mismo `UniversidadController.cargarUniversidad(universidadId)`, reutilizado.
- [`editarReferenciaBibliografica()`](../editarReferenciaBibliografica/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
