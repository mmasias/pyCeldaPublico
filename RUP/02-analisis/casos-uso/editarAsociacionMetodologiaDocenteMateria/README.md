<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsociacionMetodologiaDocenteMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarAsociacionMetodologiaDocenteMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md): sin `<<choice>>` -- edita el único campo propio de la asociación `MetodologiaMateria`, `descripcionPropia`. `codigo`/`descripcion` de la `MetodologiaDocente` se muestran de solo lectura, se editan desde `editarMetodologiaDocente()` (`Admin`, fuera de alcance).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarAsociacionMetodologiaDocenteMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarAsociacionMetodologiaDocenteMateriaView`

**Responsabilidades:**
- presenta `codigo`/`descripcion` de la `MetodologiaDocente` (solo lectura) y `descripcionPropia` (editable).
- ofrece la navegación a solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorPrograma` solicita editar la asociación.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera la asociación `MetodologiaMateria` (`cargarAsociacion(materiaId, metodologiaDocenteId)`).
- guarda la nueva `descripcionPropia` (`guardarDescripcionPropia(materiaId, metodologiaDocenteId, descripcionPropia)`).

**Colaboraciones:**
- **Entrada:** `EditarAsociacionMetodologiaDocenteMateriaView`.
- **Salida:** `MetodologiaMateriaRepository`.

## Clases de modelo

### `MetodologiaMateria`

**Responsabilidades:**
- actualiza `descripcionPropia` (`actualizar(descripcionPropia)`) -- único campo editable de la asociación, patrón catálogo+override.

**Colaboraciones:**
- **Entrada:** `MateriaController`, vía `MetodologiaMateriaRepository`.

### `MetodologiaMateriaRepository`

**Responsabilidades:**
- recupera la asociación por `Materia`/`MetodologiaDocente` (`obtener(materiaId, metodologiaDocenteId)`).
- persiste los cambios (`actualizar(metodologiaMateria)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `MetodologiaMateria`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarAsociacionMetodologiaDocenteMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaMateria{descripcionPropia}`.
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) -- crea la asociación con `descripcionPropia` vacía, que este caso de uso completa después.
