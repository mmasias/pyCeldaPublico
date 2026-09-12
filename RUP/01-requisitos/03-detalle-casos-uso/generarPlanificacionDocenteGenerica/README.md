<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > generarPlanificacionDocenteGenerica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Confirmación|Bloqueo (planificación no vacía)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/wireframe-confirmacion.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/wireframe-bloqueo.svg)|
|||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` (heredado por `DirectorGrado`)|
|**Objetivo**|Arrancar la planificación docente de una `Guia` vacía creando de golpe el mínimo de `Sesion` que exige la regla `c3`, listas para editar|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso de la familia de [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)): arranque de la planificación docente en bloque, con persistencia real e inmediata (un commit), a diferencia del CRUD de L10 ([`crearSesion()`](../crearSesion/README.md)/[`editarSesion()`](../editarSesion/README.md)/[`eliminarSesion()`](../eliminarSesion/README.md)) que queda en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md). Donde `importarPlanificacionDocenteDeGuiaHermana()` copia de una hermana `Aprobada`, este copia de nada: crea una rejilla plana de sesiones vacías. Resuelve el arranque en frío -- una guía nueva llega a la planificación docente con la tabla vacía y el medidor en rojo (`0 sesiones (mínimo 25) (faltan 25)`), y crear 25 sesiones a mano una a una antes siquiera de saber el temario es fricción pura.

Reutilizado por `DirectorGrado`, misma ficha (`DirectorGrado --|> Profesor`), no redeclarado -- igual que `importarPlanificacionDocenteDeGuiaHermana()`, y por el mismo motivo: la planificación docente no está en el [diagrama de contexto de `DirectorGrado`](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml). Actor efectivo: `Profesor` de la `AsignaturaGrado` de la guía.

**`generarPlanificacionDocenteGenerica`, verbo del catálogo**: `generar` ya es verbo propio (`generarGuiasPDF()` es el precedente exacto -- producir un artefacto derivado a partir de una entidad ya existente). El sustantivo es `PlanificacionDocente`, concepto del [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) (igual que en `importarPlanificacionDocenteDeGuiaHermana()`), no `Sesiones`. `Generica` es calificador del sustantivo: nombra la naturaleza del artefacto producido -- una plantilla sin contenido real, no una planificación docente cualquiera. Ver [Nomenclatura](/RUP/01-requisitos/01-actores-casos-uso/README.md).

**Cantidad = `Guia.sesiones_minimas`**: se crean exactamente tantas `Sesion` como el umbral de la regla `c3` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)) -- `Guia.sesiones_minimas`, snapshot de `AsignaturaGrado.sesiones_minimas` al nacer la guía, editable por el `Admin` sobre la `AsignaturaGrado`. No un `30` fijo: el número se adapta al umbral de cada guía, y el efecto observable es que el medidor de [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) pasa de rojo a verde de una (`N / N`, exactamente el mínimo).

**Cada `Sesion` creada**: `tipo = CLASE_TEORICA` (valor por defecto, el más común), `descripcion` vacía, `numero` correlativo `1..N`, y **`vinculada = True` directo** -- a diferencia de `crearSesion()`, que nace con `vinculada = False` y solo se consolida al persistir la guía. Aquí es una acción de arranque en bloque, no una edición incremental: las filas cuentan para el medidor desde el primer momento, mismo criterio que las copias de `importarPlanificacionDocenteDeGuiaHermana()`. El `Profesor` ajusta luego el `tipo` y rellena la `descripcion` de cada fila con `editarSesion()`, o borra las que sobren con `eliminarSesion()`.

**`<<choice>>` -- solo con la planificación docente vacía**: la rama verde exige que la `Guia` no tenga ninguna `Sesion` (ni vinculada ni pendiente). Si ya tiene, rama roja -- mensaje de bloqueo, sin crear nada. El botón que dispara el caso de uso solo se ofrece en el estado vacío de [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md), así que la rama roja es salvaguarda estructural (revalidación server-side), no un camino que la interfaz recorra -- mismo molde que el `<<choice>>` de [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md). Ambas ramas (roja y verde) devuelven al mismo estado, `PLANIFICACION_DOCENTE_ABIERTO`: self-loop único en el diagrama de contexto, sin transición de fallo aparte (a diferencia de `iniciarSesion()`/`enviarGuiaARevision()`, cuyo fallo tiene postcondición distinta).

**Sin degradado de la `Guia`**: una `Guia` con la planificación docente vacía nunca puede estar `Aprobada` -- la regla `c3` de `enviarGuiaARevision()` exige `>= sesiones_minimas` `Sesion` vinculadas para siquiera enviar a revisión, así que no hay estado `Aprobada` del que degradar. La operación no toca `Guia.estado` ni `fecha_generacion_pdf`; sí actualiza `fecha_ultima_modificacion`.

**Rastro**: una sola fila de `HistorialCambio` (`campo="planificacion_docente"`, `comentario="planificación docente generada (N sesiones genéricas)"`), por la operación completa -- misma traza que `importarPlanificacionDocenteDeGuiaHermana()`, coherente con que es persistencia real en bloque y no el patrón en-memoria-hasta-guardar del CRUD de L10.

**Confirmación ligera, sin `<<choice>>` de cancelación de negocio**: el sistema muestra cuántas sesiones va a crear y el `Profesor` confirma o cancela (flecha azul, sin cambios) -- misma forma que la pantalla de confirmación de `eliminarSesion()`. No es una bifurcación de validación (esa es el `<<choice>>` de vacío), es la única pregunta explícita que el caso de uso plantea.

**Fuera de alcance -- "generar desde plantilla" (patrón semanal)**: crear N sesiones con un reparto de `tipo` según un patrón (p. ej. 2 teóricas + 1 práctica por semana) es una extensión posterior. El MVP es la rejilla plana de N filas `CLASE_TEORICA`. El endpoint deja sitio a un parámetro `patron` opcional futuro sin construirlo (ver [Diseño](/RUP/03-diseño/casos-uso/generarPlanificacionDocenteGenerica/README.md)).

**Divergencia lateral registrada** (no la resuelve este caso de uso): el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) declara `Guia *-- PlanificacionDocente *-- Sesion`, pero el código aplana `Sesion` colgando directamente de `Guia` (`Sesion.guia_id`). Este caso de uso opera sobre `Sesion.guia_id` como el resto del código -- no añade lógica que dependa de una `PlanificacionDocente` intermedia. El nombre del caso de uso sí usa `PlanificacionDocente` (el concepto del modelo), no `Sesiones`.

**Guía canónica**: `GII__IYA003` (Programación I, `sesiones_minimas` = 25) como destino, con la planificación docente vacía -- estado de arranque real de una guía recién creada.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : generarPlanificacionDocenteGenerica()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente *-- Sesion`, aplanamiento a `Sesion.guia_id` en el código
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla desde la que se dispara este caso de uso (self-loop sobre `PLANIFICACION_DOCENTE_ABIERTO`), botón solo en el estado vacío
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- caso de uso de la misma familia (arranque en bloque), copia de una hermana `Aprobada` en vez de una rejilla vacía
- [`crearSesion()`](../crearSesion/README.md) / [`editarSesion()`](../editarSesion/README.md) / [`eliminarSesion()`](../eliminarSesion/README.md) -- CRUD incremental sobre las `Sesion` generadas
- [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- regla `c3` (`Guia.sesiones_minimas`), que fija la cantidad que se crea
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- familia de importación/arranque de la planificación docente
