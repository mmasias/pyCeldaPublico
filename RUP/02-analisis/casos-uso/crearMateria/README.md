<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/README.md): CRUD real e inmediato contra `MateriaRepository`. Un único campo obligatorio (`nombre`) y sin `<<choice>>` -- `Materia` no tiene ninguna regla de negocio documentada en el modelo de dominio. Mismo patrón exacto que [`crearUniversidad()`](../crearUniversidad/README.md): formulario nombre-only, salida única vía `<<include>> editarMateria()` (la transición de salida lleva la nota `editarMateria()`, regla de Requisitos). La única diferencia estructural es el punto de entrada: `Programa *-- Materia` es composición, así que la creación vive anidada bajo el `Programa` -- el `programaId` llega del contexto del listado, no lo elige el `Admin` (mismo criterio que [`crearPrograma()`](../crearPrograma/README.md) aplicó con `Facultad`). Primera escritura de `Admin` sobre `Materia`; da el punto de partida sin el cual [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md) no tendría Materias donde colgar filas.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearMateriaView`

**Responsabilidades:**
- presenta el formulario de creación: `nombre`, obligatorio.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:MATERIAS_ABIERTO` -- el `Admin` solicita crear una `Materia` desde el listado del `Programa` abierto (variante Admin de [`abrirMaterias()`](../abrirMaterias/README.md)).
- **Control:** `MateriaController`.
- **Salida:** `:Collaboration EditarMateria` vía `<<include>> editarMateria()`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- valida que `nombre` esté presente (`validarDatosObligatorios(nombre)`).
- crea la `Materia` directamente en `MateriaRepository`, real e inmediato (`crearMateria(nombre)`); el `programaId` de la composición viaja implícito en el contexto de la llamada.

**Colaboraciones:**
- **Entrada:** `CrearMateriaView`.
- **Salida:** `MateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre` y su `programaId` de composición desde el momento de crearse. Sin `estado` propio: `Materia` no se extingue (cambiar el reparto de una `Materia` de un `Programa` implica un `Programa` nuevo, no una edición del existente).

**Colaboraciones:**
- **Entrada:** creada por `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- crea la `Materia` (`crear(nombre, programaId)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/wireframes.puml) -- fuente de verdad del formulario nombre-only, salida única sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : crearMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Materia`, `Materia{nombre}`.
- [`editarMateria()`](../editarMateria/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.
- [`crearUniversidad()`](../crearUniversidad/README.md) -- mismo patrón exacto de creación nombre-only con salida única vía `<<include>>`.
- [`abrirMaterias()`](../abrirMaterias/README.md) -- listado Admin que sirve de punto de entrada, construido en este mismo lote.
