<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Profesor (edición propia)|DirectorGrado (revisión)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/wireframe-profesor.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/wireframe-revision.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Consultar los datos de la `Guia` de una `AsignaturaGrado` propia|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml): además de la entrada heredada de `Profesor` (`ASIGNATURAS_GRADO_ABIERTO`), lo reutiliza también desde `GUIAS_DEL_GRADO_ABIERTO` al revisar las guías de su grado (`consultarEstadoGuias()`, `aprobarGuia()`, `rechazarGuia()`, etc., todos de L9).

**Alcance deliberadamente mínimo hasta L7**: `abrirGuia()` fue el primer caso de uso que mostró el detalle completo de una `Guia`, pero al cerrarlo dos de sus tres composiciones reales (`PonderacionEvaluacion`, `ReferenciaBibliografica`) todavía no tenían caso de uso propio. El wireframe se limitaba a los metadatos propios de `Guia` (`semestre`, `estado`, `fechaCreacion`, `fechaUltimaModificacion`, `fechaGeneracionPDF`) y a lo heredado de `AsignaturaGrado` sin edición propia (`contenido`, `ResultadoAprendizaje`, `MetodologiaDocente`), sin sección de Evaluación ni de Bibliografía. Mismo criterio que [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md): su versión de L5 tampoco mostraba profesorado ni asociaciones hasta que L6 construyó esos casos de uso.

**Retocado al construir L8** (mismo mecanismo que el retoque de `abrirAsignaturaGrado()` en L6, sin tocar la especificación): añadidas las secciones de Evaluación y Bibliografía, con los datos reales ya usados en [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md)/[`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md). **A diferencia del retoque de `abrirAsignaturaGrado()` en L6, aquí las tablas son de solo lectura, sin botón por fila**: `GUIA_ABIERTO` solo tiene dibujada en `diagramaContextoProfesor.puml` la transición a la lista completa (`abrirPonderacionesEvaluacion()`/`abrirReferenciasBibliograficas()`), no una transición directa a `editarPonderacionEvaluacion()`/`eliminarPonderacionEvaluacion()` ni equivalentes -- esas viven un nivel más adentro, sobre `PONDERACIONES_EVALUACION_ABIERTO`/`PONDERACION_EVALUACION_ABIERTO`. Un botón `[Editar]`/`[Eliminar]` por fila aquí mismo no correspondería a ninguna transición real de la especificación (regla de oro: el wireframe corresponde exactamente a lo que modela la especificación, ni un botón de más). Cada sección lleva un único botón de navegación (`[Gestionar evaluación]`/`[Gestionar bibliografía]`) que invoca la transición ya existente hacia el listado completo, donde sí vive la gestión fila a fila.

Botones de las dos acciones de la `Guia` ya construidas: [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) y [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), ambas self-loop sobre `GUIA_ABIERTO`. `[Volver a mis asignaturas]` es [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) -- sale sin garantía de persistencia de lo que quedó en memoria, a diferencia de las otras dos. Modelado originalmente como `completarGestion()` genérico; corregido al planificar Análisis (discussion [#47](https://github.com/mmasias/pyCelda/discussions/47)) -- el destino ya tenía nombre propio.

**Retocado al construir L9**: segunda pantalla (`abrirGuia-wireframe-revision`) para el contexto de revisión de `DirectorGrado`, alcanzado vía `consultarEstadoGuias()` en vez de `ASIGNATURAS_GRADO_ABIERTO` -- mismo `GUIA_ABIERTO`, mismos datos de la `Guia`, pero con la fila de botones cambiada: sin `[Guardar borrador]`/`[Enviar a revisión]` (acciones de autor, exclusivas de `Profesor` sobre su propia guía), con las decisiones de revisión en su lugar. La pantalla mostrada usa `GII__IYA003` hipotéticamente `EnRevision` (ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44)), por eso ofrece `[Aprobar]`/`[Rechazar]` -- si la `Guia` estuviera `Borrador`/`Rechazada` el botón sería `[Escalar a aprobada]` ([`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md)), y si estuviera `Aprobada`, `[Revocar aprobación]` ([`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md)) -- un único botón de decisión ofrecido según `Guia.estado`, no las tres a la vez, mismo criterio de disponibilidad condicional que decide si se ofrece `[Descargar PDF]` (ausente aquí porque `fechaGeneracionPDF` está vacía, ver [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md)). `[Editar semestre]` ([`editarSemestreGuia()`](../editarSemestreGuia/README.md)) se ofrece siempre, sin condición de estado. `[Volver al listado de guías]` es `consultarEstadoGuias()`, no `abrirAsignaturasGrado()` -- el retorno de la familia de revisión, no el del `Profesor`.

**Profesorado, añadido al wireframe (issue [#212](https://github.com/mmasias/pyCelda/issues/212))**: la nota "Alcance deliberadamente mínimo hasta L7" de arriba describe el wireframe tal como quedó en L7, antes de que el pipeline de `Profesor` en `Guia` existiera. El campo `Profesorado` sí se construyó después (el `AbrirGuiaResponse` real lo expone desde antes de #206), pero el wireframe nunca se actualizó para reflejarlo -- deriva detectada y cerrada aquí, en ambas variantes (`abrirGuia-wireframe-profesor`/`-revision`), justo debajo de `Estado`, mismo orden que la pantalla real.

**`Profesorado` en vivo y banner de re-revisión administrativa (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: en las dos variantes, `Profesorado` deja de leer la copia `Guia -- Profesor` y pasa a leer `AsignaturaGrado -- Profesor` **en vivo** -- lo que el `Profesor` que edita y el `DirectorGrado` que revisa deben ver es lo que quedará fijado en la próxima aprobación, no una copia que puede haber quedado por detrás de la plantilla si el `Admin` la cambió. La copia congelada solo la sigue usando el PDF/previsualización oficial (ver [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md)). Cuando una `Guia` está `EnRevision` **porque el `Admin` cambió el profesorado** (transición `Aprobada -> EnRevision` administrativa, efecto colateral de `asignar`/`desasignarProfesorAAsignaturaGrado()`), aparece un **banner**: `"En revisión por cambio en los profesores que la imparten"` -- propiedad calculada análoga a `comentario_rechazo`/`comentario_revocacion` (lee la última fila de `HistorialCambio` y la expone en `AbrirGuiaResponse` cuando `estado == "EnRevision"` y esa última transición fue `Aprobada -> EnRevision` con `autor` centinela). Le dice al `DirectorGrado` que basta re-aprobar (un clic) para sincronizar la copia.

**Retrocedido a Modelo/Requisitos (discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)), tras el arranque de las pruebas reales con profesorado**: `contenido` deja de ser un campo heredado de solo lectura y pasa a ser un apartado propio de la `Guia` que el profesor edita cada curso. En `abrirGuia-wireframe-profesor` es un `textarea` editable (sembrado del curso anterior o de `AsignaturaGrado.contenido` al nacer la guía en `activarCursoAcademico()`), persistido por [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) junto con el resto del formulario y arrastrado por [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md); editable en `Borrador`/`Rechazada` y desde `Aprobada` por la reapertura ya existente (`guardarBorradorGuia()` dispara `Aprobada -> Borrador`). Cada edición real del texto genera una fila de `HistorialCambio` (`campo="contenido"`). En `abrirGuia-wireframe-revision` el mismo `contenido` se muestra en **solo lectura** -- el `DirectorGrado` lo contrasta contra el temario oficial de `AsignaturaGrado`, no lo edita (para eso tiene [`editarAsignaturaGrado()`](../editarAsignaturaGrado/README.md), que no se toca). `editarSemestreGuia()` tampoco cambia -- sigue siendo exclusivo del director para `semestre`.

**Contenido de las secciones, idéntico entre las dos pantallas** (salvo `contenido`, editable para el profesor y de solo lectura para el revisor -- ver arriba): la única otra diferencia real entre `abrirGuia-wireframe-profesor` y `abrirGuia-wireframe-revision` es la fila de botones -- las diez referencias bibliográficas (2 Básica, 3 Complementaria, 4 Webs de referencia, 1 Otras fuentes de consulta, mismo dato real de `GII__IYA003` que [`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md)) se muestran completas en ambas. La primera versión de la pantalla de revisión las recortaba a 4 filas para no recargar la imagen; corregido a las 10 tras la revisión del lote (issue [#45](https://github.com/mmasias/pyCelda/issues/45)) -- no era una decisión deliberada de qué ve cada actor, solo una inconsistencia de wireframe sin documentar.

**Retocado tras el cierre del clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)), hallazgo de Manuel usando el producto**: añadida la sección "Actividades formativas" en ambas pantallas, de solo lectura, entre "Metodologías docentes" y "Evaluación" -- mismo dato que ya lee el render (`guia.asignatura_grado.actividades_formativas`, las 10 filas `AF1`..`AF10` con `horas`/`porcentajePresencialidad`). **Revierte una frase de la #227**: al cerrar el clúster se decidió que "el `Profesor` no ve ninguna de estas tablas... las actividades formativas llegan a su guía solo por el render" -- probado en producción, Manuel pidió que también se vean aquí. Sin edición: la rejilla editable sigue siendo exclusiva de [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) sobre `AsignaturaGrado`, no sobre la `Guia` -- mismo criterio que RA/MD, que tampoco se editan desde aquí. Sin botón de gestión (a diferencia de "Evaluación"/"Bibliografía", que sí llevan `[Gestionar...]`): no hay caso de uso de asociar/desasociar que ofrecer, las 10 filas están siempre presentes.

**`fechaCreacion`, gap de Desarrollo cerrado, sin cambio de Requisitos**: el wireframe ya mostraba `Fecha de creación` desde el cierre original de L7, y el modelo de dominio ya la declara (`Guia{..., fechaCreacion, ...}`) -- el código nunca implementó la columna, y el frontend cubría el hueco con un texto de "fuera de alcance". Se cierra ahora: `Guia.fecha_creacion` nueva, nullable, sin backfill para las 108 guías ya existentes (quedan en blanco -- ver [Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) para la decisión de migración). El wireframe no cambia -- ya era correcto.

**Badge de color de estado en la cabecera** (issue [#280](https://github.com/mmasias/pyCelda/issues/280)): las líneas `Estado:` / `Estado anterior:` / `Estado actual:` de la cabecera muestran el estado como badge de color (verde `Aprobada`, ámbar `EnRevision`, rojo `Rechazada`, neutro `Borrador`), con la etiqueta legible; el texto se queda (color aditivo). **Sin caja "Leyenda"** aquí -- guía única, el badge con etiqueta se explica solo (la leyenda vive en las pantallas de lista, ver [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md)). Las comprobaciones `guia.estado === "..."` que deciden qué botones se ofrecen no cambian. Presentación pura, misma pieza (`estadoGuia.ts` + `EstadoGuiaBadge`) que las listas.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `ASIGNATURAS_GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- misma transición heredada, más `GUIAS_DEL_GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()` propia de la revisión (L9)
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia` como clase de asociación de `(AsignaturaGrado, CursoAcademico)`, `Guia.contenido` como apartado propio (3 niveles `Asignatura` -> `AsignaturaGrado` -> `Guia`)
- [Discussion #191](https://github.com/mmasias/pyCelda/discussions/191) -- retroceso a Modelo/Requisitos: `contenido` pasa a apartado editable de la `Guia` en la fase de impartición
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- estado mostrado en pantalla
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) / [Discussion #39](https://github.com/mmasias/pyCelda/discussions/39) -- cierres de L8 que originan los datos de las secciones de Evaluación y Bibliografía añadidas en este retoque
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9: dato hipotético `EnRevision`, disponibilidad condicional de botones en la pantalla de revisión
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- clúster de `ActividadFormativa`; sección de solo lectura añadida aquí tras probar en producción
- [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) -- quien edita el dato que esta pantalla muestra de solo lectura
