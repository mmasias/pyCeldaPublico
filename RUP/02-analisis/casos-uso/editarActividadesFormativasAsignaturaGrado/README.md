<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadesFormativasAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/README.md): mismo patrón que [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) sobre la asociación `ActividadFormativaAsignaturaGrado`, con dos campos editables por fila (`horas` y `porcentajePresencialidad`, este último en rango 0-100). `<<choice>>` de validación de entrada: `horas` negativas o `porcentajePresencialidad` fuera de `[0, 100]` -> no se guarda nada. Es este nivel el que el render de la `Guia` consume (sección 4 del formulario oficial).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadesFormativasAsignaturaGradoView`

**Responsabilidades:**
- presenta las 10 `ActividadFormativa` (`codigo`/`nombre` de solo lectura) con sus `horas` y `porcentajePresencialidad` actuales editables.
- ofrece la navegación a solicitar guardar el reparto completo.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita editar las actividades formativas de la `AsignaturaGrado`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO` (reparto guardado, o valor no válido -- no se guarda nada).

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- recupera el reparto actual (`cargarActividadesFormativas(asignaturaGradoId)`).
- valida cada fila: `horas >= 0` y `0 <= porcentajePresencialidad <= 100`; si alguna falla, rechaza el guardado completo.
- aplica el nuevo reparto (`guardarActividadesFormativas(asignaturaGradoId, reparto)`) fila a fila y persiste el lote.

**Colaboraciones:**
- **Entrada:** `EditarActividadesFormativasAsignaturaGradoView`.
- **Salida:** `ActividadFormativaAsignaturaGradoRepository`.

## Clases de modelo

### `ActividadFormativaAsignaturaGrado`

**Responsabilidades:**
- actualiza sus `horas` y `porcentajePresencialidad` (`actualizar(horas, porcentajePresencialidad)`). Las 10 filas existen siempre (autopobladas a 0 al crear la `AsignaturaGrado`), no se crean ni se borran aquí.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `ActividadFormativaAsignaturaGradoRepository`.

### `ActividadFormativaAsignaturaGradoRepository`

**Responsabilidades:**
- recupera las 10 filas de asociación de una `AsignaturaGrado` (`listarDe(asignaturaGradoId)`).
- persiste el lote de cambios (`actualizarLote(actividadesFormativasAsignaturaGrado)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `ActividadFormativaAsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : editarActividadesFormativasAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaAsignaturaGrado{horas, porcentajePresencialidad}`, `(AsignaturaGrado, ActividadFormativa) .. ActividadFormativaAsignaturaGrado`.
- [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) -- medidor que contrasta la suma de estas `horas` contra las de la materia.
