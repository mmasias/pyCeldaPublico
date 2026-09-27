<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > definirDirectorGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/definirDirectorGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`definirDirectorGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/README.md): alta del rol `DirectorGrado` sobre un `Profesor` ya abierto, sin `<<choice>>` -- la cardinalidad `Grado`-`DirectorGrado` es muchos a muchos con asignación libre (discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)): un `Grado` admite varios directores y un `Profesor` puede dirigir varios. El formulario tiene un único selector de `Grado` que solo ofrece los que el `Profesor` todavía no dirige. `DirectorGrado` no es una entidad que se cree en vacío: se resuelve por el email del `Profesor` y se crea si no existía, y la asignación es idempotente -- pedir lo que ya se dirige no duplica ni falla.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/definirDirectorGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DefinirDirectorGradoView`

**Responsabilidades:**
- presenta el selector de `Grado` -- solo los que el `Profesor` no dirige todavía.
- permite solicitar nombrar.

**Colaboraciones:**
- **Entrada:** `:PROFESOR_ABIERTO` -- el `Admin` solicita nombrar director de Grado desde el detalle del `Profesor`.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO` (self-loop) -- "Grado añadido a los que dirige".

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga los `Grado` disponibles (`cargarGradosDisponibles(profesorId)`) -- resuelve el rol por email y excluye los que ya dirige.
- ejecuta la asignación (`definirDirectorGrado(profesorId, gradoId)`) -- recupera `Profesor` y `Grado`, resuelve el `DirectorGrado` por email (creándolo si no existía) y añade el `Grado` a los que dirige si no estaba ya.

**Colaboraciones:**
- **Entrada:** `DefinirDirectorGradoView`.
- **Salida:** `ProfesorRepository`, `DirectorGradoRepository`, `GradoRepository`.

## Clases de modelo

### `DirectorGrado`

**Responsabilidades:**
- porta el rol -- se identifica por el mismo `email` que el `Profesor` sobre el que recae (relación denormalizada, no herencia de tabla).

**Colaboraciones:**
- **Entrada:** resuelto/creado por `DirectorGradoRepository`; asociado a `Grado`.

### `Grado`

**Responsabilidades:**
- incorpora al `DirectorGrado` a su colección `directores` (muchos a muchos).

**Colaboraciones:**
- **Entrada:** recuperado por `GradoRepository`; mutado por `ProfesorController`.

### `ProfesorRepository` / `DirectorGradoRepository` / `GradoRepository`

**Responsabilidades:**
- `ProfesorRepository.obtener(profesorId)` y `GradoRepository.obtener(gradoId)` -- los dos extremos de la asignación.
- `DirectorGradoRepository.obtenerPorEmail(email)` / `.crear(email)` -- resolución del rol con creación bajo demanda.
- `GradoRepository.listarDisponiblesParaDirigir(directorGradoId)` -- los `Grado` que quedan fuera del conjunto que ya dirige.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestionan `Profesor` / `DirectorGrado` / `Grado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorGrado/wireframes.puml) -- fuente de verdad del selector único con exclusión de los ya dirigidos.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : definirDirectorGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado o- DirectorGrado` (agregación, muchos a muchos).
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del flujo desde el Profesor, cardinalidad libre y ausencia de `<<choice>>`.
- [`quitarDirectorGrado()`](../quitarDirectorGrado/README.md) -- caso de uso complementario (baja del rol, con `<<choice>>`).
- [`abrirProfesor()`](../abrirProfesor/README.md) -- el detalle que aloja el botón de entrada.
