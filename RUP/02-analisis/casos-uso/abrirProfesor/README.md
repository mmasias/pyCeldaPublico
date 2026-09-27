<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirProfesor/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirProfesor()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el detalle de un `Profesor` -- `nombre` y `email` -- más la sección "Grados que dirige": la tabla de `Grado` de los que es `DirectorGrado`, con `[Quitar]` por fila y `[+ Nombrar director de Grado]`. Esa sección hace que el detalle no sea una carga de una sola entidad: el rol se resuelve por email contra `DirectorGrado` y de ahí a los `Grado` que dirige (`Grado o- DirectorGrado`, muchos a muchos).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirProfesor/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirProfesorView`

**Responsabilidades:**
- presenta `nombre` y `email` del `Profesor`.
- presenta la sección "Grados que dirige" (`Grado` con `[Quitar]` por fila) y el botón `[+ Nombrar director de Grado]` -- entrada a `quitarDirectorGrado()`/`definirDirectorGrado()`.
- ofrece `[Editar]` y `[Volver al listado]`.

**Colaboraciones:**
- **Entrada:** `:PROFESORES_ABIERTO` -- el `Admin` solicita abrir un `Profesor` del listado.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO`.

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga el `Profesor` (`cargarProfesor(profesorId)`).
- carga los `Grado` que dirige (`cargarGradosDirigidos(profesorId)`) -- resuelve el rol por email y lista los `Grado` del `DirectorGrado` resultante; sin `DirectorGrado` para ese email, la sección queda vacía.

**Colaboraciones:**
- **Entrada:** `AbrirProfesorView`.
- **Salida:** `ProfesorRepository`, `DirectorGradoRepository`, `GradoRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email` -- la información presentada en el detalle; el `email` es además la llave con la que se resuelve su rol de `DirectorGrado`.

**Colaboraciones:**
- **Entrada:** recuperada por `ProfesorRepository`.

### `DirectorGradoRepository` / `GradoRepository`

**Responsabilidades:**
- `DirectorGradoRepository` resuelve el rol por email (`obtenerPorEmail(email)`).
- `GradoRepository` lista los `Grado` que dirige (`listarDirigidosPor(directorGradoId)`) -- el mismo método que alimenta `abrirGrados()` del hilo `DirectorGrado`.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `DirectorGrado` / `Grado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/wireframes.puml) -- fuente de verdad del detalle con "Grados que dirige".
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESOR_ABIERTO : abrirProfesor()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado o- DirectorGrado` (muchos a muchos), `DirectorGrado -u-|> Profesor` (hereda email).
- [`definirDirectorGrado()`](../definirDirectorGrado/README.md) / [`quitarDirectorGrado()`](../quitarDirectorGrado/README.md) -- acciones sobre la sección que este detalle presenta.
- [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md) -- contraste: detalle de una sola entidad, sin sección de rol lateral.
