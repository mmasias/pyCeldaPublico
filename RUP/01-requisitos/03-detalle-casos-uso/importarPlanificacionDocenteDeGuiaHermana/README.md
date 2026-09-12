<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDeGuiaHermana/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Reemplazar la planificación docente de la `Guia` abierta con la de una `Guia` `Aprobada` de una `AsignaturaGrado` hermana|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso gemelo de [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) -- misma mecánica, misma autorización, sobre `Sesion` en vez de `ReferenciaBibliografica`. Dos casos de uso separados, no uno con parámetro: escalarán distinto (decisión de Manuel en el hilo del issue [#184](https://github.com/mmasias/pyCelda/issues/184)). Toda la ficha de `importarBibliografiaDeGuiaHermana()` aplica aquí -- a continuación solo lo específico de la planificación docente.

Reutilizado por `DirectorGrado`, misma ficha (`DirectorGrado --|> Profesor`), no redeclarado. Actor efectivo: `Profesor` de la `AsignaturaGrado` destino.

**`AsignaturaGrado` hermana**: misma doble comprobación -- mismo `asignatura_id` (FK del issue [#181](https://github.com/mmasias/pyCelda/issues/181), no nula) y mismo `Asignatura.codigo`.

**Origen**: una `Guia` en estado `Aprobada` de una `AsignaturaGrado` hermana; desplegable con el origen plenamente identificado (grado, código, nombre de la hermana, fecha de aprobación, número de sesiones) si hay más de una; botón ausente si ninguna.

**Copia con reemplazo total, real e inmediata** (a diferencia de [`crearSesion()`](../crearSesion/README.md)/[`editarSesion()`](../editarSesion/README.md)/[`eliminarSesion()`](../eliminarSesion/README.md), que quedan en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)): borra **todas** las `Sesion` de la `Guia` destino -- vinculadas y tecleadas a mano -- y crea filas nuevas copiando `tipo` y `descripcion` de las de la guía origen, replicando el flag `vinculada` de cada fila origen tal cual. Operación atómica, un solo commit.

**Renumeración `1..N` en persistencia**: las `Sesion` copiadas se renumeran `1..N` en el orden `numero` del origen, y ese número queda persistido en `Sesion.numero` -- a diferencia de [`eliminarSesion()`](../eliminarSesion/README.md), donde la renumeración es solo posicional (de presentación) y `Sesion.numero` conserva el valor de alta. Aquí las filas son nuevas, la numeración secuencial desde 1 es su valor de alta, no un reajuste. **`Guia.sesiones_minimas` del destino NO se toca**: es config de la propia `AsignaturaGrado` destino (umbral de la regla `c3` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)), puede diferir legítimamente del de la hermana; tras importar, el medidor "N / M sesiones" refleja el conteo real contra el umbral propio.

**Guía destino `Aprobada`**: se permite y se degrada a `Borrador` (mismo mecanismo que `guardarBorradorGuia()`).

**Rastro**: una sola fila de `HistorialCambio` (`campo="planificacion_docente"`), origen identificado en el comentario.

**Relajación acotada de la 404-uniforme**: idéntica a la del caso gemelo -- lectura de la planificación docente de una `Guia` `Aprobada` de una hermana, solo para listar y elegir origen. Previsualización fila a fila **diferida**.

**Divergencia lateral registrada** (no la resuelve este caso de uso): el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) declara `Guia *-- PlanificacionDocente *-- Sesion` (`PlanificacionDocente` como entidad propia), pero el código aplana `Sesion` colgando directamente de `Guia` (`Sesion.guia_id`). Este caso de uso opera sobre `Sesion.guia_id` como el resto del código -- no añade lógica que dependa de una `PlanificacionDocente` intermedia, no empeora el aplanamiento. El nombre del caso de uso sí usa `PlanificacionDocente` (el concepto del modelo), no `Sesiones`.

**Guía canónica**: `GII__IYA003` como destino, `GIOI__IYA003` (`Aprobada`) como origen -- par hermano real del piloto.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : importarPlanificacionDocenteDeGuiaHermana()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente *-- Sesion`, aplanamiento a `Sesion.guia_id` en el código, hermandad
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla desde la que se dispara este caso de uso (self-loop sobre `PLANIFICACION_DOCENTE_ABIERTO`)
- [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) -- caso de uso gemelo, ficha completa de la mecánica compartida
- [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- regla `c3` (`Guia.sesiones_minimas`) que este caso de uso no altera
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- diseño cerrado con el usuario
