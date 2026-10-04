<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarProfesor/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarProfesor()`](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/README.md): CRUD real contra `ProfesorRepository`, sin `<<choice>>`. `nombre` y `email` son ambos siempre editables (a diferencia de `editarMetodologiaDocente()`, que bloquea el `codigo` tras crear): los dos datos se piden juntos en el alta y siguen editables aquí. El `email` es único en el catálogo, así que el guardián del guardado es la unicidad del nuevo email -- si ya lo usa otro `Profesor`, el guardado no procede; con el propio, sí.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarProfesor/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarProfesorView`

**Responsabilidades:**
- presenta el formulario precargado con los datos actuales: `nombre` y `email`, ambos editables y obligatorios.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:PROFESOR_ABIERTO` -- el `Admin` solicita editar el `Profesor` abierto.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO` (self-loop -- el caso de uso no navega a otra pantalla).

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga el `Profesor` a editar (`cargarProfesor(profesorId)`).
- valida que `nombre` y `email` estén presentes (`validarDatosObligatorios(nombre, email)`).
- comprueba que el nuevo `email` no esté en uso por otro `Profesor` (`emailEnUsoPorOtro(email, profesorId)`) -- excluye el propio id: reenviar el email vigente no es un conflicto.
- guarda los cambios (`guardarCambios(profesorId, nombre, email)`).

**Colaboraciones:**
- **Entrada:** `EditarProfesorView`.
- **Salida:** `ProfesorRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- actualiza sus dos datos (`actualizar(nombre, email)`).

**Colaboraciones:**
- **Entrada:** recuperada y mutada vía `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- resuelve si el email lo usa otro (`obtenerPorEmailDeOtro(email, profesorId)`).
- persiste la edición (`editar(profesor)`).

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `Profesor`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/wireframes.puml) -- fuente de verdad del formulario con ambos campos precargados.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : editarProfesor()`.
- [`crearProfesor()`](../crearProfesor/README.md) -- el alta que fija los dos mismos campos.
- [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md) -- contraste: campo identificador bloqueado tras crear; aquí no hay campo bloqueado.
