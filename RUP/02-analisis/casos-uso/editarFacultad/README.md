<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarFacultad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarFacultad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarFacultad()`](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/README.md): CRUD real e inmediato contra `FacultadRepository`, mismo patrón que [`editarUniversidad()`](../editarUniversidad/README.md) un nivel arriba. Sin `<<choice>>` -- `Facultad` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo el obligatorio `nombre`. `Facultad` gana aquí su método `actualizar(nombre)`. Es también el destino del `<<include>>` de [`crearFacultad()`](../crearFacultad/README.md): tras crear, el `Admin` queda editando la `Facultad` recién creada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarFacultad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarFacultadView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la `Facultad` (`nombre`).
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:FACULTAD_ABIERTO` -- el `Admin` solicita editar la `Facultad` abierta; también alcanzado como `<<include>>` de `crearFacultad()`.
- **Control:** `FacultadController`.
- **Salida:** `:FACULTAD_ABIERTO`.

## Clases de controlador

### `FacultadController`

**Responsabilidades:**
- recupera la `Facultad` a editar (`cargarFacultad(facultadId)`, mismo método introducido por [`abrirFacultad()`](../abrirFacultad/README.md)).
- valida el obligatorio (`validarDatosObligatorios(nombre)`).
- guarda los cambios (`guardarCambios(facultadId, nombre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente a la `Facultad` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarFacultadView`.
- **Salida:** `Facultad`, `FacultadRepository`.

## Clases de modelo

### `Facultad`

**Responsabilidades:**
- porta `nombre`, editable.
- se actualiza a sí misma (`actualizar(nombre)`) -- mismo patrón que `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** persistida por `FacultadRepository`.

### `FacultadRepository`

**Responsabilidades:**
- recupera la `Facultad` por identificador (`obtener(facultadId)`).
- persiste la actualización (`actualizar(facultad)`).

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** gestiona `Facultad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTAD_ABIERTO --> FACULTAD_ABIERTO : editarFacultad()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad *-d- Facultad`, `Facultad *-d- Programa`.
- [`crearFacultad()`](../crearFacultad/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí.
- [`abrirFacultad()`](../abrirFacultad/README.md) -- mismo `FacultadController.cargarFacultad(facultadId)`, reutilizado.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- mismo patrón un nivel arriba.
