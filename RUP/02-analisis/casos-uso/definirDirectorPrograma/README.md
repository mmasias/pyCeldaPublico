<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > definirDirectorPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/definirDirectorPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`definirDirectorPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/README.md): alta del rol `DirectorPrograma` sobre un `Profesor` ya abierto, sin `<<choice>>` -- la cardinalidad `Programa`-`DirectorPrograma` es muchos a muchos con asignación libre (discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)): un `Programa` admite varios directores y un `Profesor` puede dirigir varios. El formulario tiene un único selector de `Programa` que solo ofrece los que el `Profesor` todavía no dirige. `DirectorPrograma` no es una entidad que se cree en vacío: se resuelve por el email del `Profesor` y se crea si no existía, y la asignación es idempotente -- pedir lo que ya se dirige no duplica ni falla.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/definirDirectorPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DefinirDirectorProgramaView`

**Responsabilidades:**
- presenta el selector de `Programa` -- solo los que el `Profesor` no dirige todavía.
- permite solicitar nombrar.

**Colaboraciones:**
- **Entrada:** `:PROFESOR_ABIERTO` -- el `Admin` solicita nombrar director de Programa desde el detalle del `Profesor`.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO` (self-loop) -- "Programa añadido a los que dirige".

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga los `Programa` disponibles (`cargarProgramasDisponibles(profesorId)`) -- resuelve el rol por email y excluye los que ya dirige.
- ejecuta la asignación (`definirDirectorPrograma(profesorId, programaId)`) -- recupera `Profesor` y `Programa`, resuelve el `DirectorPrograma` por email (creándolo si no existía) y añade el `Programa` a los que dirige si no estaba ya.

**Colaboraciones:**
- **Entrada:** `DefinirDirectorProgramaView`.
- **Salida:** `ProfesorRepository`, `DirectorProgramaRepository`, `ProgramaRepository`.

## Clases de modelo

### `DirectorPrograma`

**Responsabilidades:**
- porta el rol -- se identifica por el mismo `email` que el `Profesor` sobre el que recae (relación denormalizada, no herencia de tabla).

**Colaboraciones:**
- **Entrada:** resuelto/creado por `DirectorProgramaRepository`; asociado a `Programa`.

### `Programa`

**Responsabilidades:**
- incorpora al `DirectorPrograma` a su colección `directores` (muchos a muchos).

**Colaboraciones:**
- **Entrada:** recuperado por `ProgramaRepository`; mutado por `ProfesorController`.

### `ProfesorRepository` / `DirectorProgramaRepository` / `ProgramaRepository`

**Responsabilidades:**
- `ProfesorRepository.obtener(profesorId)` y `ProgramaRepository.obtener(programaId)` -- los dos extremos de la asignación.
- `DirectorProgramaRepository.obtenerPorEmail(email)` / `.crear(email)` -- resolución del rol con creación bajo demanda.
- `ProgramaRepository.listarDisponiblesParaDirigir(directorProgramaId)` -- los `Programa` que quedan fuera del conjunto que ya dirige.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestionan `Profesor` / `DirectorPrograma` / `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/wireframes.puml) -- fuente de verdad del selector único con exclusión de los ya dirigidos.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : definirDirectorPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o- DirectorPrograma` (agregación, muchos a muchos).
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del flujo desde el Profesor, cardinalidad libre y ausencia de `<<choice>>`.
- [`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md) -- caso de uso complementario (baja del rol, con `<<choice>>`).
- [`abrirProfesor()`](../abrirProfesor/README.md) -- el detalle que aloja el botón de entrada.
