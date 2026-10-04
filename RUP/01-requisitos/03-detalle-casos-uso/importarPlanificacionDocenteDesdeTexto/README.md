<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md) / [Diseño](/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDesdeTexto()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|[Diseño](/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Reemplazar la planificación docente de la `Guia` abierta con la que el `Profesor` pega como texto, una `Sesion` por línea|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso hermano de [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md): misma operación (reemplazo total de las `Sesion` de la `Guia` abierta), distinto origen -- aquí texto pegado, no otra `Guia`. Sin `AsignaturaPrograma` hermana, sin desplegable de orígenes y sin relajación de la 404-uniforme: el origen lo aporta el propio `Profesor` en la petición. Implementado en el issue [#552](https://github.com/mmasias/pyCelda/issues/552) (PR [#553](https://github.com/mmasias/pyCelda/pull/553)); esta ficha documenta el rastro RUP del código ya mergeado (issue [#554](https://github.com/mmasias/pyCelda/issues/554)).

Reutilizado por `DirectorPrograma`, misma ficha (`DirectorPrograma --|> Profesor`), no redeclarado. Actor efectivo: `Profesor` de la `AsignaturaPrograma` de la `Guia` destino (`AsignaturaProgramaRepository.imparte`; si no, 404 uniforme).

**Formato del texto**: una `Sesion` por línea, `CODIGO - Descripción`. El separador es el **primer** ` - ` (espacio-guion-espacio) de la línea. El código se normaliza con `strip()` + `upper()` y se mapea a `Sesion.tipo`:

<div align=center>

|Código|`Sesion.tipo`|
|-|-|
|`CT`|`CLASE_TEORICA`|
|`CP`|`CLASE_PRACTICA`|
|`CTP`|`CLASE_TEORICO_PRACTICA`|
|`CL`|`CLASE_LABORATORIO`|
|`EC`|`EVALUACION_CONTINUA`|
|`EP`|`EVALUACION_PARCIAL`|

</div>

**Reglas de parseo**: las líneas vacías o solo con espacios se ignoran; no se rechaza ninguna línea. Con separador ` - ` completo, el código (parte izquierda) se busca en la tabla -- reconocido, tipo mapeado y descripción = parte derecha; no reconocido, `CLASE_TEORICA` con la línea completa. Como el corte es por la primera ocurrencia, los ` - ` posteriores forman parte de la descripción. **Sin ese separador completo** (p. ej. `"CTP -"`, `"CTP-"` o `"CTP"` sola -- típico de una fila de tipo correcto sin contenido todavía): se comprueba si lo que queda tras un guion final es un código reconocido; si lo es, se respeta ese tipo con descripción vacía. El tipo solo se descarta cuando el código no se reconoce, nunca por falta de contenido (hallazgo de Manuel, corregido tras el primer despliegue).

**Copia con reemplazo total, real e inmediata**: borra **todas** las `Sesion` de la `Guia` destino -- vinculadas y tecleadas a mano -- y crea filas nuevas `1..N` en el orden de las líneas, con `vinculada=False` (a diferencia de [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md), no hay fila origen de la que replicar el flag). La numeración `1..N` queda persistida en `Sesion.numero`. Operación atómica, un solo commit. **`Guia.sesiones_minimas` NO se toca.**

**Texto vacío**: permitido; deja la planificación docente vacía (la vista lo avisa). **Guía destino `Aprobada`**: se permite y se degrada a `Borrador` (`Guia.confirmar_guardado()`, mismo mecanismo que `guardarBorradorGuia()`).

**Rastro**: una sola fila de `HistorialCambio` (`campo="planificacion_docente"`, `valor_nuevo="N sesiones (texto pegado)"`, `comentario="planificación docente importada desde texto pegado"`).

**Divergencia lateral registrada** (no la resuelve este caso de uso): el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) declara `Guia *-- PlanificacionDocente *-- Sesion`, pero el código aplana `Sesion.guia_id`; este caso de uso opera sobre `Sesion.guia_id` como el resto del código.

**Tope de longitud de la descripción** (issue [#669](https://github.com/mmasias/pyCelda/issues/669)): cada `Sesion` creada respeta el tope de 500 caracteres de [`crearSesion()`](../crearSesion/README.md). Si la descripción de alguna línea lo supera, la importación entera se rechaza con `422` (`Línea N: la descripción supera el límite de 500 caracteres`, siendo `N` el número de línea del texto pegado, contando las vacías) y no se borra nada: no se recorta en silencio. Es una barrera de entrada, no abre rama en la especificación ni cambia la regla de que ninguna línea del parseo se descarta.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : importarPlanificacionDocenteDesdeTexto()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla desde la que se dispara este caso de uso (self-loop sobre `PLANIFICACION_DOCENTE_ABIERTO`)
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- caso de uso hermano (origen: otra `Guia`)
- [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- regla `c3` (`Guia.sesiones_minimas`) que este caso de uso no altera
- [Issue #552](https://github.com/mmasias/pyCelda/issues/552) -- implementación; [issue #554](https://github.com/mmasias/pyCelda/issues/554) -- rastro RUP
