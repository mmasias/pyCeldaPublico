<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`importarPlanificacionDocenteDeGuiaHermana()`](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md): el `Profesor` de una `AsignaturaPrograma` copia la planificación docente de una `Guia` en estado `Aprobada` de una `AsignaturaPrograma` hermana -- otra con `id` distinto, el mismo `asignaturaId` no nulo y el mismo `Asignatura.codigo` (issue [#184](https://github.com/mmasias/pyCelda/issues/184), sobre la FK al catálogo puesta en el [#181](https://github.com/mmasias/pyCelda/issues/181)). Copia con **reemplazo total**: borra TODAS las `Sesion` de la guía destino -- las vinculadas y las que el profesor destino tecleó a mano -- y crea filas nuevas con `guiaId` = destino copiando `tipo` y `descripcion`, replicando el flag `vinculada` de cada fila origen TAL CUAL -- no se fuerza a `True` (un origen `Aprobado` por el flujo normal tiene todo vinculado por la regla `c1`; sólo un origen escalado vía `escalarGuiaAAprobada()`, que bypasea `c1`, puede llevar candidatas `vinculada=False`), renumerando las `Sesion` copiadas 1..N en persistencia en el orden `numero` del origen -- y NO tocando `guia.sesiones_minimas` del destino. Real e inmediata -- persiste en el acto en un solo commit, a diferencia del CRUD de L8 que queda en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md). Si la guía destino estaba `Aprobada`, se degrada a `Borrador` (mismo mecanismo que `guardarBorradorGuia()` -> `Guia.confirmar_guardado()`) y la operación completa registra UNA fila de `HistorialCambio` (`campo="planificacion_docente"`, origen identificado en `comentario`, p.ej. "planificación docente importada desde GII / IYA003"). Autorización: relajación acotada de la regla 404-uniforme -- el `Profesor` de la `AsignaturaPrograma` destino puede LEER la planificación docente de una guía `Aprobada` de una hermana suya, sólo para listar y elegir origen; ninguna otra lectura cross-programa se abre. La previsualización del contenido fila a fila del origen antes de importar queda DIFERIDA a un refinamiento posterior: por ahora la vista informa con recuentos (sesiones que trae el origen, sesiones del destino que se reemplazarán). Divergencia lateral ya registrada: el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) modela `Guia *-- PlanificacionDocente *-- Sesion` pero el código persiste `Sesion.guia_id` directo -- este caso de uso opera sobre `Sesion.guia_id` como el resto del código, no empeora la divergencia.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ImportarPlanificacionDocenteDeGuiaHermanaView`

**Responsabilidades:**
- presenta el desplegable de guías origen candidatas: las guías `Aprobadas` de `AsignaturaPrograma` hermanas, cada una identificada por programa + código de `Asignatura` + nombre de la AG hermana + fecha de aprobación, con el recuento de sesiones que trae y el recuento de sesiones del destino que se reemplazarán.
- permite solicitar importar.

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita importar la planificación docente de una guía hermana para la `Guia` que tiene abierta; si no hay ninguna guía `Aprobada` hermana, el caso de uso no se ofrece (botón ausente).
- **Control:** `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** `:Collaboration AbrirPlanificacionDocente` vía `<<include>> abrirPlanificacionDocente()` -- vuelve al listado, ya con la planificación docente reemplazada.

## Clases de controlador

### `ImportarPlanificacionDocenteDeGuiaHermanaController`

**Responsabilidades:**
- `listarOrigenesImportables(guiaDestinoId)`: guías `Aprobadas` de hermanas con sus recuentos -- alimenta el desplegable; lista vacía = botón ausente.
- vuelve a obtener la `Guia` origen por id (`GuiaRepository.obtener(guiaOrigenId)`) y `validarHermandad(guiaDestino, guiaOrigen)`: revalidación server-side -- comprueba que `guiaOrigen.estado == "Aprobada"` y que la `AsignaturaPrograma` de origen sigue siendo hermana de la de destino (mismo `asignaturaId` no nulo y mismo `Asignatura.codigo`). El `guiaOrigenId` del cliente nunca se confía; el detalle de la respuesta (404 uniforme si no valida) se fija en Diseño.
- `importarPlanificacionDocente(guiaDestinoId, guiaOrigenId)`: orquesta el reemplazo -- borra todas las `Sesion` del destino, crea copias desde el origen replicando `vinculada` y renumerando 1..N, degrada la guía destino si estaba `Aprobada` y registra una fila de `HistorialCambio`.
- real e inmediato: toda la operación persiste en un solo commit.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDeGuiaHermanaView`.
- **Salida:** `GuiaRepository`, `AsignaturaProgramaRepository`, `Guia`, `SesionRepository`, `HistorialCambio`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `asignaturaId` (FK al catálogo `Asignatura`, issue [#181](https://github.com/mmasias/pyCelda/issues/181)) -- dos `AsignaturaPrograma` con el mismo `asignaturaId` y el mismo `Asignatura.codigo` son hermanas.

**Colaboraciones:**
- **Entrada:** gestionada por `AsignaturaProgramaRepository`.
- **Salida:** su hermandad resuelve qué guías origen son importables.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- `listarHermanas(asignaturaProgramaId)`: otras `AsignaturaPrograma` con el mismo `asignaturaId` y el mismo `codigo`, excluyendo la propia; `[]` si `asignaturaId` es nulo.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia`

**Responsabilidades:**
- `confirmar_guardado()`: degrada `Aprobada -> Borrador` si la guía destino estaba aprobada -- mecanismo reutilizado tal cual de `guardarBorradorGuia()`, la propia `Guia` decide según su máquina de estados.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- localiza la guía destino (`obtener(guiaDestinoId)`) y las guías `Aprobadas` de las hermanas (`listarAprobadasDe(hermanas)`).
- persiste la `Guia` tras el reemplazo -- posible cambio de `estado` (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** gestiona `Guia`.

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo`, `descripcion`, `vinculada` y `guiaId` -- las copias nacen como filas nuevas con `guiaId` = destino, `vinculada` replicada fila a fila del origen y `numero` renumerado 1..N en el orden `numero` del origen.

**Colaboraciones:**
- **Entrada:** leídas las del origen y creadas las del destino por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- `reemplazarDesde(guiaDestinoId, sesionesOrigen)`: borra todas las `Sesion` del destino (vinculadas y no vinculadas) y crea las copias (`tipo`, `descripcion`, `vinculada`) renumeradas 1..N en persistencia -- no toca `Guia.sesiones_minimas`; persistencia real, parte del único commit de la operación.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** gestiona `Sesion`.

### `HistorialCambio`

**Responsabilidades:**
- `registrar(campo="planificacion_docente", ...)`: UNA fila por la operación completa -- no una por sesión -- con el origen identificado en `comentario` (p.ej. "planificación docente importada desde GII / IYA003").

**Colaboraciones:**
- **Entrada:** creada por `ImportarPlanificacionDocenteDeGuiaHermanaController`.
- **Salida:** fila asociada a la `Guia` destino.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/wireframes.puml) -- fuente de verdad del desplegable de orígenes.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : importarPlanificacionDocenteDeGuiaHermana()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente *-- Sesion` (divergencia lateral con el `Sesion.guia_id` directo del código, ver Propósito).
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- mecanismo de degradado `Aprobada -> Borrador` compartido (`confirmar_guardado()`).
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla de origen del botón y retorno tras importar.
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- origen del caso de uso.
