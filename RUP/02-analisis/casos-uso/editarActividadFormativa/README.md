<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md): CRUD real e inmediato, sin ninguna colaboración con otra entidad. El `codigo` se presenta de solo lectura (regla de Requisitos: no editable una vez creada la actividad); efectivamente solo cambia `nombre`. Sin `<<choice>>`: la única validación es de forma (`codigo` y `nombre` presentes). `ActividadFormativa` gana el método `actualizar(codigo, nombre)`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarActividadFormativaView`

**Responsabilidades:**
- presenta los datos actuales: `codigo` (solo lectura) y `nombre`.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDAD_FORMATIVA_ABIERTO` -- el `Admin` solicita editar la `ActividadFormativa` abierta.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDAD_FORMATIVA_ABIERTO` con los datos actualizados.

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- carga la `ActividadFormativa` (`cargarActividadFormativa(actividadFormativaId)`).
- valida los datos obligatorios (`validarDatosObligatorios(codigo, nombre)`).
- guarda los cambios (`guardarCambios(actividadFormativaId, codigo, nombre)`): actualiza el modelo y persiste en el repositorio (`editar(actividadFormativa)`).

**Colaboraciones:**
- **Entrada:** `EditarActividadFormativaView`.
- **Salida:** `ActividadFormativa`, `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- se actualiza a sí misma (`actualizar(codigo, nombre)`).

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`; mutada por `ActividadFormativaController`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- recupera la `ActividadFormativa` (`obtener(actividadFormativaId)`) y persiste la editada (`editar(actividadFormativa)`).

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/wireframes.puml) -- fuente de verdad de el formulario de edición, con `codigo` de solo lectura..
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDAD_FORMATIVA_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : editarActividadFormativa()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo de `Universidad` (`Universidad *-- ActividadFormativa`).
- [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md) -- clúster plantilla.
- [`abrirActividadFormativa()`](../abrirActividadFormativa/README.md) -- detalle desde el que se edita.
- [`editarAsignatura()`](../editarAsignatura/README.md) -- mismo patrón de carga previa + guardado sin `<<choice>>`.
