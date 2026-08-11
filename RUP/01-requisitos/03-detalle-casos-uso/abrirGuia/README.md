<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

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

Botones de las dos acciones de la `Guia` ya construidas: [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) y [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), ambas self-loop sobre `GUIA_ABIERTO`. `[Volver a mis asignaturas]` es `completarGestion()`, transición de navegación no catalogada -- sale sin garantía de persistencia de lo que quedó en memoria, a diferencia de las otras dos.

**Retocado al construir L9**: segunda pantalla (`abrirGuia-wireframe-revision`) para el contexto de revisión de `DirectorGrado`, alcanzado vía `consultarEstadoGuias()` en vez de `ASIGNATURAS_GRADO_ABIERTO` -- mismo `GUIA_ABIERTO`, mismos datos de la `Guia`, pero con la fila de botones cambiada: sin `[Guardar borrador]`/`[Enviar a revisión]` (acciones de autor, exclusivas de `Profesor` sobre su propia guía), con las decisiones de revisión en su lugar. La pantalla mostrada usa `GII__IYA003` hipotéticamente `EnRevision` (ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44)), por eso ofrece `[Aprobar]`/`[Rechazar]` -- si la `Guia` estuviera `Borrador`/`Rechazada` el botón sería `[Escalar a aprobada]` ([`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md)), y si estuviera `Aprobada`, `[Revocar aprobación]` ([`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md)) -- un único botón de decisión ofrecido según `Guia.estado`, no las tres a la vez, mismo criterio de disponibilidad condicional que decide si se ofrece `[Descargar PDF]` (ausente aquí porque `fechaGeneracionPDF` está vacía, ver [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md)). `[Editar semestre]` ([`editarSemestreGuia()`](../editarSemestreGuia/README.md)) se ofrece siempre, sin condición de estado. `[Volver al listado de guías]` es `consultarEstadoGuias()`, no `completarGestion()` -- el retorno de la familia de revisión, no el del `Profesor`.

**Contenido de las secciones, idéntico entre las dos pantallas**: la única diferencia real entre `abrirGuia-wireframe-profesor` y `abrirGuia-wireframe-revision` es la fila de botones -- las diez referencias bibliográficas (2 Basica, 3 Complementaria, 4 WebsReferencia, 1 OtrasFuentes, mismo dato real de `GII__IYA003` que [`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md)) se muestran completas en ambas. La primera versión de la pantalla de revisión las recortaba a 4 filas para no recargar la imagen; corregido a las 10 tras la revisión del lote (issue [#45](https://github.com/mmasias/pyCelda/issues/45)) -- no era una decisión deliberada de qué ve cada actor, solo una inconsistencia de wireframe sin documentar.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `ASIGNATURAS_GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- misma transición heredada, más `GUIAS_DEL_GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()` propia de la revisión (L9)
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- Modelo del dominio -- `Guia` como clase de asociación de `(AsignaturaGrado, CursoAcademico)`, herencia de `contenido` sobre `AsignaturaGrado`
- Diagrama de estados de Guia -- estado mostrado en pantalla
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) / [Discussion #39](https://github.com/mmasias/pyCelda/discussions/39) -- cierres de L8 que originan los datos de las secciones de Evaluación y Bibliografía añadidas en este retoque
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9: dato hipotético `EnRevision`, disponibilidad condicional de botones en la pantalla de revisión
