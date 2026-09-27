<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarResultadoAprendizajeAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md): sin `<<choice>>` -- asocia real e inmediato un `ResultadoAprendizaje` del catálogo del `Grado` a una `Materia`. Primer escalón de la cascada `Grado`->`Materia`->`AsignaturaGrado`. A diferencia de `asociarMetodologiaDocenteAMateria()`, la asociación (`Materia o-u- ResultadoAprendizaje`) es simple, sin clase de asociación ni atributo propio -- no hay `editarAsociacionX()` en este par.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarResultadoAprendizajeAMateriaView`

**Responsabilidades:**
- presenta la selección de `ResultadoAprendizaje` del `Grado` todavía no asociados a esta `Materia`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorGrado` solicita asociar un `ResultadoAprendizaje`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` del `Grado` todavía no asociados a la `Materia` (`cargarResultadosAprendizajeDisponibles(materiaId)`).
- asocia real e inmediato (`asociarResultadoAprendizaje(materiaId, resultadoAprendizajeId)`) -- agregación simple, sin clase de asociación que crear.

**Colaboraciones:**
- **Entrada:** `AsociarResultadoAprendizajeAMateriaView`.
- **Salida:** `MateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- gana un `ResultadoAprendizaje` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `MateriaController`, vía `MateriaRepository`.
- **Salida:** compone `ResultadoAprendizaje` asociados.

### `MateriaRepository`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` del `Grado` todavía no asociados a una `Materia` (`listarResultadosAprendizajeDisponibles(materiaId)`).
- persiste la nueva asociación (`asociarResultadoAprendizaje(materiaId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarResultadoAprendizajeAMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-u- ResultadoAprendizaje`.
- [`desasociarResultadoAprendizajeAMateria()`](../desasociarResultadoAprendizajeAMateria/README.md) -- caso de uso complementario (baja de la asociación).
- [`asociarResultadoAprendizajeAAsignaturaGrado()`](../asociarResultadoAprendizajeAAsignaturaGrado/README.md) -- segundo escalón de la misma cascada.
