<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarSistemaEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/README.md): CRUD real e inmediato contra `SistemaEvaluacionRepository`. Sin `<<choice>>` -- no hay regla de negocio documentada en Requisitos más allá de la obligatoriedad de `tipo`, `ponderacionMinima` y `ponderacionMaxima` (`codigo` y `descripcion` opcionales); la coherencia del rango `0 <= mínima <= máxima <= 100` es, igual que en el alta, validación de forma de la Vista. Todos los campos son editables, sin campo fijo desde el alta -- `codigo` (issue #772) es el de la memoria, no un identificador interno, y puede faltar hasta que lo cargue la importación del RUCT. `SistemaEvaluacion` gana aquí su método `actualizar(codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima)`, mismo patrón que `MetodologiaDocente.actualizar(codigo, descripcion)`; el existente `validarMaximo(ponderacion)` (usado por `PonderacionEvaluacion`) queda intacto.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarSistemaEvaluacionView`

**Responsabilidades:**
- presenta el formulario con los datos actuales del `SistemaEvaluacion` (`codigo`, `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`), los cinco precargados y editables.
- valida la coherencia del rango antes de solicitar guardar (validación de forma).
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_EVALUACION_ABIERTO` -- el `Admin` solicita editar el `SistemaEvaluacion` abierto; también es el destino del alta de [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md).
- **Control:** `SistemaEvaluacionController`.
- **Salida:** `:SISTEMA_EVALUACION_ABIERTO`.

## Clases de controlador

### `SistemaEvaluacionController`

**Responsabilidades:**
- recupera el `SistemaEvaluacion` a editar (`cargarSistemaEvaluacion(sistemaEvaluacionId)`, mismo método introducido por [`abrirSistemaEvaluacion()`](../abrirSistemaEvaluacion/README.md)).
- valida los obligatorios (`validarDatosObligatorios(tipo, ponderacionMinima, ponderacionMaxima)` -- el mismo método ya usado en crear).
- guarda los cambios (`guardarCambios(sistemaEvaluacionId, codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima)`): sin `<<choice>>` de negocio que aplicar -- pide directamente al `SistemaEvaluacion` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarSistemaEvaluacionView`.
- **Salida:** `SistemaEvaluacion`, `SistemaEvaluacionRepository`.

## Clases de modelo

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`.
- se actualiza a sí misma (`actualizar(codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima)`) -- mismo patrón que `MetodologiaDocente.actualizar(codigo, descripcion)`.

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** persistida por `SistemaEvaluacionRepository`.

### `SistemaEvaluacionRepository`

**Responsabilidades:**
- recupera el `SistemaEvaluacion` por identificador (`obtener(sistemaEvaluacionId)`).
- persiste la actualización (`editar(sistemaEvaluacion)`).

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** gestiona `SistemaEvaluacion`.

**Actor `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: misma colaboración, con la comprobación de que la `Materia` pertenece a un programa que dirige.

**Guarda de rango (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: crear un sistema o cambiar su rango se rechaza (409) si alguna `Guia` del curso activo En revisión o Aprobada de la `Materia` dejaría de cumplir la regla de `Guia.bloqueo_ponderaciones()` para ese sistema -- suma de sus `PonderacionEvaluacion` vinculadas en [mínima, máxima]; un sistema nuevo cuenta como 0 %. Las guías en Borrador o Rechazada no cuentan: se revalidan en `enviarGuiaARevision()`. Sin esta guarda, estrechar un rango invalidaba en silencio guías ya validadas.


**`codigo` (issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: `SistemaEvaluacion` gana `codigo`, el de la memoria verificada (p. ej. `E1`), opcional; vacío se guarda como nulo, sin unicidad que comprobar. `descripcion` pasa a ser la denominación literal de la memoria: la clase no cambia de forma, cambia el significado del dato.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : editarSistemaEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `SistemaEvaluacion{codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima}`.
- [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md) -- el alta alcanza el detalle desde el que se edita, sin `<<include>>` C->U.
- [`abrirSistemaEvaluacion()`](../abrirSistemaEvaluacion/README.md) -- mismo `SistemaEvaluacionController.cargarSistemaEvaluacion(sistemaEvaluacionId)`, reutilizado.
- [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio; allí `codigo` fijo desde el alta, aquí todos los campos editables, `codigo` incluido.
