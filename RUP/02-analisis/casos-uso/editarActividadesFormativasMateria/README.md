<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md): el `DirectorGrado` edita las `horas` de las 10 filas `ActividadFormativaMateria` de una `Materia` en una sola operación (rejilla). `codigo`/`nombre` de cada `ActividadFormativa` se muestran de solo lectura -- catálogo institucional de `Universidad`, no se editan desde aquí. `<<choice>>` de validación de entrada: si alguna `horas` es negativa no se guarda nada. La regla `AfM = Σ AfAdM` **no** se comprueba aquí (blanda, vive en [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadesFormativasMateriaView`

**Responsabilidades:**
- presenta las 10 `ActividadFormativa` (`codigo`/`nombre` de solo lectura) con sus `horas` actuales editables.
- ofrece la navegación a solicitar guardar el reparto completo.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorGrado` solicita editar las actividades formativas de la `Materia`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO` (reparto guardado, o algún valor de `horas` no válido -- no se guarda nada).

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera el reparto actual (`cargarActividadesFormativas(materiaId)`).
- valida que ninguna `horas` sea negativa; si alguna lo es, rechaza el guardado completo.
- aplica el nuevo reparto (`guardarActividadesFormativas(materiaId, repartoHoras)`) fila a fila y persiste el lote.

**Colaboraciones:**
- **Entrada:** `EditarActividadesFormativasMateriaView`.
- **Salida:** `ActividadFormativaMateriaRepository`.

## Clases de modelo

### `ActividadFormativaMateria`

**Responsabilidades:**
- actualiza sus `horas` (`actualizar(horas)`) -- único campo editable de la asociación. Las 10 filas existen siempre (autopobladas a 0 al crear la `Materia`), no se crean ni se borran aquí.

**Colaboraciones:**
- **Entrada:** `MateriaController`, vía `ActividadFormativaMateriaRepository`.

### `ActividadFormativaMateriaRepository`

**Responsabilidades:**
- recupera las 10 filas de asociación de una `Materia` (`listarDe(materiaId)`).
- persiste el lote de cambios (`actualizarLote(actividadesFormativasMateria)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `ActividadFormativaMateria`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarActividadesFormativasMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas}`, `(Materia, ActividadFormativa) .. ActividadFormativaMateria`.
- [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) -- el mismo patrón un nivel más abajo, con `porcentajePresencialidad` además de `horas`.
