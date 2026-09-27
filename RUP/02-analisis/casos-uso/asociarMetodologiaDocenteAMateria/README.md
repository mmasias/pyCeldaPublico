<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarMetodologiaDocenteAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md): patrón C→U, sin `<<choice>>` -- crea real e inmediato la asociación `MetodologiaMateria` entre una `Materia` y una `MetodologiaDocente` del catálogo institucional, con `descripcionPropia` vacía por defecto (se completa después en [`editarAsociacionMetodologiaDocenteMateria()`](../editarAsociacionMetodologiaDocenteMateria/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarMetodologiaDocenteAMateriaView`

**Responsabilidades:**
- presenta la selección de `MetodologiaDocente` del catálogo institucional todavía no asociadas a esta `Materia`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorGrado` solicita asociar una `MetodologiaDocente`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- lista las `MetodologiaDocente` del catálogo todavía no asociadas a la `Materia` (`cargarMetodologiasDocentesDisponibles(materiaId)`).
- crea real e inmediata la asociación `MetodologiaMateria` (`asociarMetodologiaDocente(materiaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `AsociarMetodologiaDocenteAMateriaView`.
- **Salida:** `MetodologiaDocenteRepository`, `MetodologiaMateriaRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- el catálogo institucional del que se elige.

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista las `MetodologiaDocente` del catálogo institucional todavía no asociadas a una `Materia` (`listarDisponiblesParaMateria(materiaId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `MetodologiaDocente`.

### `MetodologiaMateria`

**Responsabilidades:**
- porta `descripcionPropia`, vacía en el momento de crearse -- clase de asociación entre `Materia` y `MetodologiaDocente`.

**Colaboraciones:**
- **Entrada:** creada por `MetodologiaMateriaRepository`.

### `MetodologiaMateriaRepository`

**Responsabilidades:**
- crea real e inmediata la asociación (`crear(materiaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `MetodologiaMateria`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarMetodologiaDocenteAMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- MetodologiaDocente` vía `MetodologiaMateria{descripcionPropia}`.
- [`editarAsociacionMetodologiaDocenteMateria()`](../editarAsociacionMetodologiaDocenteMateria/README.md) -- quien completa `descripcionPropia` después.
- [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) -- caso de uso complementario (baja de la asociación).
