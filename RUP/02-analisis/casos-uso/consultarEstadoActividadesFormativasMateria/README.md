<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`consultarEstadoActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md): caso de uso de **solo lectura**, sin `<<choice>>`. Presenta el estado de la regla `AfM = Σ AfAdM` de una `Materia` -- por cada `ActividadFormativa`, las `horas` de la materia frente a la suma de las `horas` de sus `AsignaturaPrograma`, con las discrepancias marcadas -- y, desde el issue [#772](https://github.com/mmasias/pyCelda/issues/772), el total de horas de la materia frente a 25 h por ECTS cuando la `Materia` tiene `ects`. Los dos cálculos viven en el modelo (`Materia.discrepanciasActividadesFormativas()` y `Materia.comprobacionHorasEcts()`, Fat Model -- mismo sitio que `Guia.bloqueo_ponderaciones()`), no en el controlador ni en un servicio. Ninguno reparte ni bloquea nada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ConsultarEstadoActividadesFormativasMateriaView`

**Responsabilidades:**
- presenta las `ActividadFormativa` del catálogo del `Programa` con `horas` de la materia, suma de las de sus `AsignaturaPrograma` y la diferencia; resalta las que no cuadran.
- presenta, si la `Materia` tiene `ects`, sus horas frente a las esperadas (`ects × 25`) y la diferencia.
- deja claro que el medidor es informativo -- no bloquea ningún guardado.
- ofrece la navegación a volver a la `Materia`.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorPrograma` solicita consultar el estado de las actividades formativas (desde la sección compuesta en `abrirMateria()`).
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera la `Materia` con sus `ActividadFormativaMateria` y las `ActividadFormativaAsignaturaPrograma` de sus `AsignaturaPrograma` (`cargarEstadoActividadesFormativas(materiaId)`).
- delega el cálculo de discrepancias y la comprobación por ECTS en el modelo; no valida ni muta nada -- solo lectura.

**Colaboraciones:**
- **Entrada:** `ConsultarEstadoActividadesFormativasMateriaView`.
- **Salida:** `MateriaRepository`, `Materia`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- calcula, por cada `ActividadFormativa`, `horas` de la materia vs `Σ horas` de sus `AsignaturaPrograma`, y marca las que no cuadran (`discrepanciasActividadesFormativas()`). Método de dominio (Fat Model), mismo patrón que `Guia.bloqueo_ponderaciones()` -- pero puramente informativo, no hay envío ni transición que bloquear.
- compara la suma de `horas` de sus `ActividadFormativaMateria` con `ects × 25` (`comprobacionHorasEcts()`): `ects`, horas esperadas, horas de la materia, si cuadra y la diferencia; nada si no tiene `ects`.

**Colaboraciones:**
- **Entrada:** `MateriaController`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` con la cascada que el cálculo recorre (`ActividadFormativaMateria`, `AsignaturaPrograma` -> `ActividadFormativaAsignaturaPrograma`) mediante carga anticipada (`obtener(materiaId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: misma colaboración con `Admin` como iniciador, sin comprobación de programa propio.


## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframes.puml) -- fuente de verdad.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : consultarEstadoActividadesFormativasMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas, porcentajePresencialidad}`, `ActividadFormativaAsignaturaPrograma{horas}`, `Materia.ects`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo y de la forma (read agregado sin mutación).
