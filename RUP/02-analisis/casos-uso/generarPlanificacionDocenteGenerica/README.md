<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > generarPlanificacionDocenteGenerica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/generarPlanificacionDocenteGenerica/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`generarPlanificacionDocenteGenerica()`](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/README.md): el `Profesor` de una `AsignaturaGrado` arranca la planificación docente de su `Guia` -- que está **vacía** -- creando de golpe tantas `Sesion` como el mínimo que exige la regla `c3` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) (`Guia.sesiones_minimas`, snapshot de la `AsignaturaGrado`, no un `30` fijo). Cada `Sesion` nace con `tipo="CLASE_TEORICA"`, `descripcion=""`, `numero` correlativo `1..N` y `vinculada=True` **directo** -- a diferencia de [`crearSesion()`](../crearSesion/README.md), que nace con `vinculada=False` y solo se consolida al persistir la guía: aquí es una acción de arranque en bloque, no una edición incremental, y las filas cuentan para el medidor desde el primer momento (mismo criterio que las copias de [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md)). Real e inmediata -- persiste en el acto en un solo commit, a diferencia del CRUD de L10 que queda en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md). La operación completa registra UNA fila de `HistorialCambio` (`campo="planificacion_docente"`, `comentario="planificación docente generada (N sesiones genéricas)"`), coherente con `importarPlanificacionDocenteDeGuiaHermana()` (misma familia, issue [#184](https://github.com/mmasias/pyCelda/issues/184)). No hay degradado de estado: una `Guia` con la planificación docente vacía nunca puede estar `Aprobada` (la regla `c3` exige `>= sesiones_minimas` `Sesion` vinculadas para siquiera enviar a revisión), así que `Guia.estado` y `fecha_generacion_pdf` no se tocan; sí se actualiza `fecha_ultima_modificacion`. Precondición de validación (rama roja de la especificación): si la planificación docente **no** está vacía -- alguna `Sesion`, vinculada o pendiente -- el sistema bloquea sin crear nada. El botón que dispara el caso de uso solo se ofrece en el estado vacío de [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md), así que esa rama es salvaguarda estructural (revalidación server-side), no un camino que la interfaz recorra -- molde de [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md). Autorización: regla 404-uniforme sin relajación (a diferencia de `importarPlanificacionDocenteDeGuiaHermana()`, que sí lee cross-grado) -- solo el `Profesor` que imparte la `AsignaturaGrado` de la guía; cualquier otro, 404. Divergencia lateral ya registrada: el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) modela `Guia *-- PlanificacionDocente *-- Sesion` pero el código persiste `Sesion.guia_id` directo -- este caso de uso opera sobre `Sesion.guia_id` como el resto del código.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/generarPlanificacionDocenteGenerica/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `GenerarPlanificacionDocenteGenericaView`

**Responsabilidades:**
- presenta el número de `Sesion` que se van a crear (`Guia.sesiones_minimas`) y una nota de que todas nacen como `CLASE_TEORICA` sin descripción, editables después.
- permite solicitar confirmar o cancelar la generación.
- no se muestra si la planificación docente ya tiene sesiones (el botón de entrada, en `abrirPlanificacionDocente()`, solo aparece en el estado vacío).

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita generar una planificación docente genérica para la `Guia` que tiene abierta.
- **Control:** `GenerarPlanificacionDocenteGenericaController`.
- **Salida:** `:Collaboration AbrirPlanificacionDocente` vía `<<include>> abrirPlanificacionDocente()` -- vuelve al listado, ya con las `Sesion` genéricas creadas y el medidor en verde.

## Clases de controlador

### `GenerarPlanificacionDocenteGenericaController`

**Responsabilidades:**
- obtiene la `Guia` por id (`GuiaRepository.obtener(guiaId)`) y verifica que el `Profesor` la imparte (404 uniforme si no).
- comprueba `Guia.planificacionDocenteVacia()`: si es `False`, responde con el detalle de conflicto (409, el detalle exacto se fija en Diseño) sin crear nada.
- `generarGenerica(guiaId)`: orquesta la creación -- pide a `SesionRepository` las `N = guia.sesionesMinimas` filas genéricas, registra una fila de `HistorialCambio` y actualiza `fecha_ultima_modificacion` de la `Guia`.
- real e inmediato: toda la operación persiste en un solo commit.

**Colaboraciones:**
- **Entrada:** `GenerarPlanificacionDocenteGenericaView`.
- **Salida:** `GuiaRepository`, `Guia`, `SesionRepository`, `HistorialCambio`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- `planificacionDocenteVacia() : boolean`: `True` si la `Guia` no tiene ninguna `Sesion` (ni vinculada ni pendiente) -- precondición de la rama verde.
- porta `sesionesMinimas` (snapshot de `AsignaturaGrado.sesiones_minimas`), que fija cuántas `Sesion` se crean.
- `confirmarGuardado()`: aquí solo actualiza `fecha_ultima_modificacion` -- una `Guia` con planificación docente vacía nunca está `Aprobada`, no hay transición `Aprobada -> Borrador` que disparar (a diferencia de `importarPlanificacionDocenteDeGuiaHermana()`).

**Colaboraciones:**
- **Entrada:** `GenerarPlanificacionDocenteGenericaController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- localiza la `Guia` (`obtener(guiaId)`) y la persiste tras la generación (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GenerarPlanificacionDocenteGenericaController`.
- **Salida:** gestiona `Guia`.

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo`, `descripcion`, `vinculada` y `guiaId` -- las genéricas nacen con `guiaId` = la guía, `tipo="CLASE_TEORICA"`, `descripcion=""`, `vinculada=True` y `numero` `1..N`.

**Colaboraciones:**
- **Entrada:** creadas en bloque por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- `generarGenericas(guia, cantidad) : lista de Sesion`: crea `cantidad` filas nuevas `CLASE_TEORICA` sin descripción, vinculadas, numeradas `1..cantidad` -- simétrico a `reemplazarDesde()` de `importarPlanificacionDocenteDeGuiaHermana()` pero sin borrado previo (la precondición garantiza que no hay nada que borrar). Persistencia real, parte del único commit de la operación.

**Colaboraciones:**
- **Entrada:** `GenerarPlanificacionDocenteGenericaController`.
- **Salida:** gestiona `Sesion`.

### `HistorialCambio`

**Responsabilidades:**
- `registrar(campo="planificacion_docente", ...)`: UNA fila por la operación completa -- no una por sesión -- con `comentario="planificación docente generada (N sesiones genéricas)"`.

**Colaboraciones:**
- **Entrada:** creada por `GenerarPlanificacionDocenteGenericaController`.
- **Salida:** fila asociada a la `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/README.md) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/wireframes.puml) -- fuente de verdad del comportamiento y la pantalla de confirmación.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : generarPlanificacionDocenteGenerica()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente *-- Sesion` (divergencia lateral con el `Sesion.guia_id` directo del código, ver Propósito).
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- misma familia (arranque en bloque), copia de una hermana `Aprobada`; comparte `SesionRepository` y la traza de `HistorialCambio`.
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla de origen del botón (estado vacío) y retorno tras generar.
- [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- regla `c3` (`sesiones_minimas`), que fija la cantidad.
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- familia de importación/arranque de la planificación docente.
