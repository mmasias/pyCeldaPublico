<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirProfesor/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirProfesor()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el detalle de un `Profesor` -- `nombre` y `email` -- más la sección "Programas que dirige": la tabla de `Programa` de los que es `DirectorPrograma`, con `[Quitar]` por fila y `[+ Nombrar director de Programa]`. Esa sección hace que el detalle no sea una carga de una sola entidad: el rol se resuelve por email contra `DirectorPrograma` y de ahí a los `Programa` que dirige (`Programa o- DirectorPrograma`, muchos a muchos).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirProfesor/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirProfesorView`

**Responsabilidades:**
- presenta `nombre` y `email` del `Profesor`.
- presenta la sección "Programas que dirige" (`Programa` con `[Quitar]` por fila) y el botón `[+ Nombrar director de Programa]` -- entrada a `quitarDirectorPrograma()`/`definirDirectorPrograma()`.
- ofrece `[Editar]` y `[Volver al listado]`.

**Colaboraciones:**
- **Entrada:** `:PROFESORES_ABIERTO` -- el `Admin` solicita abrir un `Profesor` del listado.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO`.

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga el `Profesor` (`cargarProfesor(profesorId)`).
- carga los `Programa` que dirige (`cargarProgramasDirigidos(profesorId)`) -- resuelve el rol por email y lista los `Programa` del `DirectorPrograma` resultante; sin `DirectorPrograma` para ese email, la sección queda vacía.

**Colaboraciones:**
- **Entrada:** `AbrirProfesorView`.
- **Salida:** `ProfesorRepository`, `DirectorProgramaRepository`, `ProgramaRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email` -- la información presentada en el detalle; el `email` es además la llave con la que se resuelve su rol de `DirectorPrograma`.

**Colaboraciones:**
- **Entrada:** recuperada por `ProfesorRepository`.

### `DirectorProgramaRepository` / `ProgramaRepository`

**Responsabilidades:**
- `DirectorProgramaRepository` resuelve el rol por email (`obtenerPorEmail(email)`).
- `ProgramaRepository` lista los `Programa` que dirige (`listarDirigidosPor(directorProgramaId)`) -- el mismo método que alimenta `abrirProgramas()` del hilo `DirectorPrograma`.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `DirectorPrograma` / `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/wireframes.puml) -- fuente de verdad del detalle con "Programas que dirige".
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESOR_ABIERTO : abrirProfesor()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o- DirectorPrograma` (muchos a muchos), `DirectorPrograma -u-|> Profesor` (hereda email).
- [`definirDirectorPrograma()`](../definirDirectorPrograma/README.md) / [`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md) -- acciones sobre la sección que este detalle presenta.
- [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md) -- contraste: detalle de una sola entidad, sin sección de rol lateral.
