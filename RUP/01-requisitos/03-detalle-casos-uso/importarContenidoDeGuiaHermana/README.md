<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/importarContenidoDeGuiaHermana/README.md) / [Diseño](/RUP/03-diseño/casos-uso/importarContenidoDeGuiaHermana/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarContenidoDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Reemplazar el contenido (temario) de la `Guia` abierta con el de una `Guia` `Aprobada` de una `AsignaturaPrograma` hermana|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#409](https://github.com/mmasias/pyCelda/issues/409), discussion posterior a #392..#408): reflexión de Manuel con pySigHor tras cerrar esa tanda -- de las tres piezas de una `Guia` que se pueden importar de una asignatura hermana (bibliografía y planificación docente, ambas del issue [#184](https://github.com/mmasias/pyCelda/issues/184)), faltaba `contenido`. Se había descartado en su momento para `PonderacionEvaluacion` porque sus valores están acotados por `SistemaEvaluacion.ponderacionMinima`/`Maxima` de la `Materia` -- dos hermanas pueden colgar de `Materia`s con rangos distintos, importar rompería esa validación. `contenido` no tiene ese problema: es texto libre, sin ninguna validación cruzada -- mismo perfil que bibliografía/planificación docente, más portable incluso.

**Caso de uso reutilizado por `DirectorPrograma`, misma ficha** -- ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) (`DirectorPrograma --|> Profesor`), no redeclarado, mismo trato que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)/[`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md). El actor efectivo es siempre el `Profesor` de la `AsignaturaPrograma` **destino**.

**Self-loop directo de `GUIA_ABIERTO`, no de un listado propio** -- a diferencia de [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) (self-loop de `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`) e [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) (self-loop de `PLANIFICACION_DOCENTE_ABIERTO`): `contenido` es un campo escalar de la propia `Guia`, sin colección que gestionar -- no hay pantalla plural que justifique un estado propio.

**Reutiliza al completo la infraestructura del issue #184** (`backend/app/routers/importar_guia_hermana.py`): mismo helper `_guia_destino_o_404()` (gate de autorización -- el `Profesor` debe impartir la `AsignaturaPrograma` destino, mismo criterio 404-uniforme relajado solo para leer orígenes hermanos), mismo `_origen_o_404()`, mismo `_identificador_origen()`, mismo schema `ImportarDeGuiaHermanaRequest`/`GuiaResponse` (sin schema nuevo). `Guia.actualizar_contenido()` (ya existente, usado también por [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)) devuelve el valor anterior solo si el texto cambió -- una importación que trae el mismo contenido no genera fila de `HistorialCambio` ("no-op sin fila").

**Reemplazo total y atómico, un solo commit** -- mismo criterio que bibliografía/planificación docente: sustituye por completo el contenido, no fusiona. Una única fila de `HistorialCambio` (`campo="contenido"` -- campo **ya existente**, compartido con la edición manual vía [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md), no suma etiqueta nueva a la Auditoría), con el origen identificado en el comentario. El temario es texto largo y `HistorialCambio.valor_*` es corto (`String(50)`) -- se guarda un resumen con los espacios colapsados y truncado a 47 caracteres + "...", el detalle completo del cambio vive en `Guia.contenido`, no en la auditoría.

**Guía destino `Aprobada`**: se permite importar y la `Guia` se degrada a `Borrador` -- mismo mecanismo (`Guia.confirmar_guardado()`) que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md).

**UI deliberadamente ligera** -- "algo ligero y rápido: botón y a tomar por saco" (Manuel, sesión previa a #423): control inline en [`abrirGuia()`](../abrirGuia/README.md) (`AbrirGuia.tsx`), select + botón tras el textarea de Contenido, sin pantalla ni ruta propia. Sin recuento de referencias ni fecha de aprobación en la opción del desplegable (a diferencia de bibliografía, que sí las muestra) -- solo programa/código/nombre de la asignatura hermana. Sin previsualización del contenido antes de importar, aviso genérico tras seleccionar origen ("esto reemplazará el contenido actual, incluidos cambios sin guardar"), no un recuento como en bibliografía.

**Punto crítico de implementación**: el contenido del textarea vive en estado local (React) hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- tras importar, el frontend actualiza ese estado local con la respuesta del `POST`, para que un guardado posterior no pise en silencio el contenido recién importado con el valor viejo que seguía en pantalla.

**Solo visible al `Profesor` autor, nunca en modo revisor**: el control no aparece cuando `AbrirGuia.tsx` está en modo revisión (`DirectorPrograma` evaluando la `Guia` de otro) -- ese modo no edita contenido y `get_current_profesor_id` no resuelve para esa sesión. Un `DirectorPrograma` que además imparte sí lo ve, sobre su propia `Guia`, por el mismo camino de autor que usa `Profesor`.

**Se suma retroactivamente a L7** (`Guia`, apertura/borrador): `contenido` es atributo propio de `Guia` desde el cierre original de esa capa -- mismo tipo de hueco que [`consultarHistorialCambios()`](../consultarHistorialCambios/README.md) destapó en L8.

**Documentado con retraso** (desplegado el 2026-09-15, ficha escrita el 2026-09-18): quedó fuera del dashboard de seguimiento al construirse en la misma sesión que el cierre de #392..#408, sin checkpoint de prosa RUP aparte -- hallado al auditar el catálogo real de producción durante el cierre de #423/#425.

## Notas de diseño y trazabilidad

- Control ligero, sin pantalla ni ruta propia, sin previsualización de origen ni recuento (a diferencia de [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md)). Solo es visible para el Profesor autor, nunca en modo revisor. Planteamiento acordado con Manuel: un botón y nada más.

- Modelado: a diferencia de `importarBibliografiaDeGuiaHermana()`/`importarPlanificacionDocenteDeGuiaHermana()` (self-loop de su propio listado, `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`/`PLANIFICACION_DOCENTE_ABIERTO`), `contenido` es un campo escalar de la propia `Guia`: self-loop directo de `GUIA_ABIERTO`, sin pantalla propia (issue [#409](https://github.com/mmasias/pyCelda/issues/409)).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : importarContenidoDeGuiaHermana()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- package Edicion, `importarContenidoDeGuiaHermana -- Profesor`
- [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) / [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- casos de uso gemelos, misma infraestructura del issue #184
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- `Guia.actualizar_contenido()`/mecanismo de degradado `Aprobada -> Borrador` compartidos
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- diseño original de la familia de importación entre hermanas
- [Issue #409](https://github.com/mmasias/pyCelda/issues/409) -- diseño de este caso de uso; [PR #410](https://github.com/mmasias/pyCelda/pull/410) -- construcción, desplegado en producción (`9732bb2`)
