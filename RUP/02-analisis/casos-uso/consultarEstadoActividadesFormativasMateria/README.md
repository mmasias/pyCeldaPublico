<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > consultarEstadoActividadesFormativasMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`consultarEstadoActividadesFormativasMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md): caso de uso de **solo lectura**, sin `<<choice>>`. Presenta el estado de la regla `AfM = Σ AfAdM` de una `Materia` -- por cada `ActividadFormativa`, las `horas` de la materia frente a la suma de las `horas` de sus `AsignaturaGrado`, con las discrepancias marcadas. El cálculo vive en el modelo (`Materia.discrepanciasActividadesFormativas()`, Fat Model -- mismo sitio que `Guia.bloqueo_ponderaciones()`), no en el controlador ni en un servicio.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ConsultarEstadoActividadesFormativasMateriaView`

**Responsabilidades:**
- presenta las 10 `ActividadFormativa` con `horas` de la materia, suma de las de sus `AsignaturaGrado` y la diferencia; resalta las que no cuadran.
- deja claro que el medidor es informativo -- no bloquea ningún guardado.
- ofrece la navegación a volver a la `Materia`.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorGrado` solicita consultar el estado de las actividades formativas (desde la sección compuesta en `abrirMateria()`).
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- recupera la `Materia` con sus `ActividadFormativaMateria` y las `ActividadFormativaAsignaturaGrado` de sus `AsignaturaGrado` (`cargarEstadoActividadesFormativas(materiaId)`).
- delega el cálculo de discrepancias en el modelo; no valida ni muta nada -- solo lectura.

**Colaboraciones:**
- **Entrada:** `ConsultarEstadoActividadesFormativasMateriaView`.
- **Salida:** `MateriaRepository`, `Materia`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- calcula, por cada `ActividadFormativa`, `horas` de la materia vs `Σ horas` de sus `AsignaturaGrado`, y marca las que no cuadran (`discrepanciasActividadesFormativas()`). Método de dominio (Fat Model), mismo patrón que `Guia.bloqueo_ponderaciones()` -- pero puramente informativo, no hay envío ni transición que bloquear.

**Colaboraciones:**
- **Entrada:** `MateriaController`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` con la cascada que el cálculo recorre (`ActividadFormativaMateria`, `AsignaturaGrado` -> `ActividadFormativaAsignaturaGrado`) mediante carga anticipada (`obtener(materiaId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/wireframes.puml) -- fuente de verdad.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : consultarEstadoActividadesFormativasMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativaMateria{horas}`, `ActividadFormativaAsignaturaGrado{horas, porcentajePresencialidad}`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo y de la forma (read agregado sin mutación).
