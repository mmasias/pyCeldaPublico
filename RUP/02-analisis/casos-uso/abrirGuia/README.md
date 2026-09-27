<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- no vincula nada. Presenta los metadatos propios de la `Guia`, su `contenido` (temario) propio -- editable por el `Profesor`, de solo lectura para el `DirectorGrado`, discussion [#191](https://github.com/mmasias/pyCelda/discussions/191) --, y las secciones de Evaluación, Bibliografía y Planificación docente **fusionando** lo ya vinculado a la `Guia` con lo pendiente-sin-vincular creado o editado en las sub-vistas (`crearPonderacionEvaluacion()`, `crearReferenciaBibliografica()`, `crearSesion()`, etc., que ya persisten real e inmediatamente contra su propio repositorio). Es el punto de entrada de la sesión de edición: el primer `GuiaRepository.obtener(guiaId)`. Trae además `Guia.sesiones_minimas` (snapshot del umbral de planificación docente, discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)) para el medidor de sesiones.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirGuiaView`

**Responsabilidades:**
- presenta los metadatos propios de la `Guia`: `semestre`, `estado`, `fechaCreacion`, `fechaUltimaModificacion`, `fechaGeneracionPDF`, y el `profesorado` (lista de email, "Sin profesorado asignado" si está vacía).
- presenta el nombre de la `AsignaturaGrado` como título de la pantalla, y sus `resultadosAprendizaje`/`metodologiasDocentes`/`actividadesFormativas` como referencia de solo lectura (secciones "Resultados de aprendizaje"/"Metodologías docentes"/"Actividades formativas") -- estructura ya gestionada por `Admin`/`DirectorGrado` en otro CU ([`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) / [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md)), aquí solo se muestra. `actividadesFormativas` es incorporación posterior (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)): al cerrar el clúster se decidió que el `Profesor` no las vería aquí, revertido tras probar en producción -- mismo criterio de solo lectura que RA/MD, sin botón de gestión.
- presenta el `contenido` (temario) propio de la `Guia` -- editable por el `Profesor` en un `textarea`, de solo lectura para el `DirectorGrado` (discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)). La persistencia del texto no la hace este caso de uso: la recoge `guardarBorradorGuia()` junto con el resto del formulario.
- presenta la sección de Evaluación: `PonderacionEvaluacion` vinculadas + pendientes, agrupadas por `SistemaEvaluacion`, con el medidor de completitud (total contra 100% y subtotal por sistema contra su rango -- discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), Bloque 1; cálculo de la Vista sobre la lista fusionada).
- presenta la sección de Bibliografía: `ReferenciaBibliografica` vinculadas + pendientes, con su `tipo` en forma legible.
- presenta la sección de Planificación docente: `Sesion` vinculadas + pendientes, ordenadas por `numero`, con el medidor "N / M sesiones" contra `Guia.sesiones_minimas` (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), Bloque 3; cálculo de la Vista).
- ofrece la navegación a la gestión de cada sección (`[Gestionar evaluación]` / `[Gestionar bibliografía]` / `[Gestionar planificación docente]`) y las acciones sobre la `Guia` (`[Guardar borrador]`, `[Enviar a revisión]`, `[Volver a mis asignaturas]`).
- si la ruta indica modo revisor (parámetro `gradoId` en la URL, no un dato de la `Guia`) pero `puedeRevisar` llega en `false`, trata la respuesta como "Guía no encontrada" -- mismo patrón 403-como-404 que el resto de la aplicación, defensa en profundidad contra un `DirectorGrado` que fuerza la URL de revisión de una `Guia` que no dirige (issue [#212](https://github.com/mmasias/pyCelda/issues/212)).

**Colaboraciones:**
- **Entrada:** `:ASIGNATURAS_GRADO_ABIERTO` -- el `Profesor` solicita abrir su `Guia`.
- **Control:** `GuiaController`.
- **Salida:** `:GUIA_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- recupera la `Guia` (`GuiaRepository.obtener(guiaId)`) para sus metadatos propios -- la misma llamada trae ya cargados `asignaturaGrado` (con `resultadosAprendizaje`/`metodologiasDocentes` y su `profesorado`), no son lecturas independientes.
- el `profesorado` que presenta la Vista sale de `asignaturaGrado.profesorado` **en vivo**, no de `guia.profesorado` (issue [#254](https://github.com/mmasias/pyCelda/issues/254)): en la sesión de edición y en la revisión se debe ver lo que quedará fijado al aprobar. Precarga `selectinload(Guia.asignaturaGrado).selectinload(AsignaturaGrado.profesorado)`.
- si `guia.estado == "EnRevision"` y la última fila de `HistorialCambio` es la transición `Aprobada -> EnRevision` administrativa (issue #254), expone el `comentario` de esa fila como banner -- propiedad calculada de `Guia`, misma familia que `comentarioRechazo`/`comentarioRevocacion`.
- pide, para cada colección, las filas ya vinculadas y las pendientes-sin-vincular por separado, y las fusiona en una sola lista por presentar -- unión simple, sin regla de negocio (no es responsabilidad de `Guia`: es agregación de lectura para la Vista, no una decisión de dominio).
- calcula `puedeRevisar` (`GradoRepository.dirige(guia.gradoId, directorGradoId)`) -- sí es una lectura independiente nueva. Reutiliza la misma comprobación que la guardia de acceso de entrada (Profesor dueño o DirectorGrado del grado), pero aquí como dato de salida para la Vista, no como guardia -- issue [#212](https://github.com/mmasias/pyCelda/issues/212).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirGuiaView`.
- **Salida:** `GuiaRepository`, `GradoRepository`, `PonderacionEvaluacionRepository`, `ReferenciaBibliograficaRepository`, `SesionRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- porta sus metadatos propios y su `contenido` (temario) propio -- sembrado de `AsignaturaGrado.contenido` o de la `Guia` del curso anterior al nacer, independiente desde entonces (discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)).
- porta `sesiones_minimas` -- snapshot del umbral de planificación docente al nacer (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)), que la Vista usa como `M` del medidor "N / M sesiones".
- expone su colección oficial de `PonderacionEvaluacion`/`ReferenciaBibliografica`/`Sesion` vinculadas (`Guia *-d- PonderacionEvaluacion`, `Guia *-- ReferenciaBibliografica`, `Guia *-- PlanificacionDocente *-- Sesion`).
- expone su `AsignaturaGrado` y, a través de ella, el `profesorado` en vivo (`asignaturaGrado.profesorado`) -- issue [#212](https://github.com/mmasias/pyCelda/issues/212) añadió estas colaboraciones; el issue [#254](https://github.com/mmasias/pyCelda/issues/254) cambia la fuente del `profesorado` de la copia `guia.profesorado` a la plantilla en vivo. La copia `Guia -- Profesor` sigue existiendo, pero solo la lee el render del PDF/previsualización.
- expone `comentarioRevisionPorProfesorado` (o análogo) -- propiedad calculada: el `comentario` de la última fila de `HistorialCambio` cuando `estado == "EnRevision"` y esa fila es la transición `Aprobada -> EnRevision` con `autor` centinela (issue #254). Misma mecánica que `comentarioRechazo`/`comentarioRevocacion`.

**Colaboraciones:**
- **Entrada:** `GuiaController`, vía `GuiaRepository`.
- **Salida:** compone `PonderacionEvaluacion`, `ReferenciaBibliografica`, `Sesion` vinculadas, `AsignaturaGrado`, `Profesor`.

### `GuiaRepository`

**Responsabilidades:**
- recupera la `Guia` por identificador (`obtener(guiaId)`), con su colección vinculada.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

### `AsignaturaGrado`

**Responsabilidades:**
- porta `nombre` (título de la pantalla) y `contenido` (referencia estructural, distinto del `contenido` propio de la `Guia` -- discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)); porta también sus `resultadosAprendizaje`/`metodologiasDocentes`/`actividadesFormativas`, mostrados de solo lectura -- gestionados por otro CU ([`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) / [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md)).

**Colaboraciones:**
- **Entrada:** cargada junto a la `Guia` por `GuiaRepository.obtener(guiaId)`, no por una lectura independiente.

### `Profesor`

**Responsabilidades:**
- porta `email` -- toda la lista se muestra unida por comas, sin detalle adicional por profesor.

**Colaboraciones:**
- **Entrada:** cargado junto a la `Guia` por `GuiaRepository.obtener(guiaId)`, no por una lectura independiente.

### `GradoRepository`

**Responsabilidades:**
- responde si un `DirectorGrado` dirige el `Grado` de la `Guia` (`dirige(gradoId, directorGradoId)`) -- misma pregunta que la guardia de acceso de entrada, aquí para producir `puedeRevisar` como dato de salida.

**Colaboraciones:**
- **Entrada:** `GuiaController`.

### `PonderacionEvaluacion`

**Responsabilidades:**
- porta `descripcion`, `ponderacion`, el enlace a su `SistemaEvaluacion` y si está vinculada -- mostrada agrupada, con la suma total calculada por la Vista a partir de la lista fusionada.

**Colaboraciones:**
- **Entrada:** listada por `PonderacionEvaluacionRepository`, vinculada o pendiente.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- lista las `PonderacionEvaluacion` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `PonderacionEvaluacion` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `PonderacionEvaluacion`.

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo`, `referencia` y si está vinculada -- mostrada agrupada por tipo, fusionando vinculadas y pendientes.

**Colaboraciones:**
- **Entrada:** listada por `ReferenciaBibliograficaRepository`, vinculada o pendiente.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- lista las `ReferenciaBibliografica` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `ReferenciaBibliografica` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo`, `descripcion` y si está vinculada -- mostrada ordenada por `numero` en la sección de Planificación docente, fusionando vinculadas y pendientes. El `numero` presentado es posición en la lista fusionada (ver [`abrirPlanificacionDocente()` en Análisis](../abrirPlanificacionDocente/README.md)).

**Colaboraciones:**
- **Entrada:** listada por `SesionRepository`, vinculada o pendiente.

### `SesionRepository`

**Responsabilidades:**
- lista las `Sesion` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `Sesion` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Sesion`.

## Simplificación fuera de alcance de esta rebanada

**Contexto de revisión de `DirectorGrado`**: la especificación de Requisitos documenta una segunda variante de wireframe (`abrirGuia-wireframe-revision`, con botones de decisión en vez de edición), alcanzada vía `consultarEstadoGuias()` desde `GUIAS_DEL_GRADO_ABIERTO`. Esta rebanada cubre el camino de autor (`Profesor`), no el de revisor -- `consultarEstadoGuias()` no se construye aquí.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `ASIGNATURAS_GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-d- PonderacionEvaluacion`, `Guia *-- ReferenciaBibliografica`, `Guia *-- PlanificacionDocente *-- Sesion`; regla agregada de planificación docente mínima (`sesiones_minimas`).
- [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) / [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) / [`crearSesion()`](../crearSesion/README.md) -- quiénes crean lo pendiente-sin-vincular que esta pantalla fusiona.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- acciones ofrecidas desde esta pantalla, quienes vinculan lo pendiente o lo borran por ausencia.
- [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) -- gestiona la estructura (`resultadosAprendizaje`/`metodologiasDocentes`) que esta pantalla solo muestra de solo lectura.
- [Issue #212](https://github.com/mmasias/pyCelda/issues/212) -- deriva de este artefacto anterior a #206, cerrada aquí: faltaban `profesorado`, `asignaturaGrado` y `puedeRevisar` en las colaboraciones de salida.
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `profesorado` pasa a leerse en vivo de `AsignaturaGrado`; banner de re-revisión administrativa (propiedad calculada, patrón `comentarioRechazo`).
