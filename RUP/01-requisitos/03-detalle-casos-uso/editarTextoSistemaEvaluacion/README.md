<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarTextoSistemaEvaluacion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarTextoSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarTextoSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Editar el texto de convocatorias (apartado 5 de la guía docente) de una `Guia` propia|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Hallazgo del debate de la discussion [#609](https://github.com/mmasias/pyCelda/discussions/609) (issue [#610](https://github.com/mmasias/pyCelda/issues/610)): el texto de "CONVOCATORIA ORDINARIA"/"CONVOCATORIA EXTRAORDINARIA" estaba hardcodeado en la plantilla de renderizado, con un placeholder sin rellenar ("pendiente de concretar") en todo documento generado. Pasa a ser dato editable de `Guia.texto_sistema_evaluacion`.

No se documenta como ampliación de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) -- edita otro atributo, con endpoint de guardado propio (`PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion`), aunque vive en la misma pantalla "Gestionar evaluación" (`PONDERACIONES_EVALUACION_ABIERTO`, no un estado propio -- no hay navegación nueva, solo una acción más sobre el mismo estado).

**Patrón B, no Patrón A** (distinción completa en la discussion #609): a diferencia de `requisitosPrevios`/`resultadosAprendizaje` (contrato con memoria de verificación, vive en `AsignaturaPrograma`, corrección excepcional), este texto describe directamente la tabla de ponderaciones de **esta** `Guia` -- evoluciona curso a curso igual que ella. `activarCursoAcademico()` lo clona de la `Guia` anterior; sin predecesora (asignatura nueva) nace vacío, sin ningún campo de respaldo en `AsignaturaPrograma`.

**`<<choice>>` de marcador único**: el texto debe contener el literal `[TABLA]` exactamente una vez -- es el punto donde el renderizado inserta la tabla real de instrumentos de evaluación. Cero apariciones dejaría la tabla fuera del documento en silencio; dos o más harían ambiguo dónde insertarla. Rama roja: `422`, texto sin cambios -- mismo mecanismo que la rama roja de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md), vuelve al mismo estado de origen.

**Tres plantillas de frontend** (asignatura normal, prácticas externas, prácticas de laboratorio) rellenan el área de texto sin guardar -- el `Profesor` las ajusta y decide. No son casos de uso propios: son valores iniciales de un único campo de formulario, mismo criterio que cualquier otro valor por defecto de un formulario.

**Datos legados**: la migración `migrar_texto_sistema_evaluacion.py` hace backfill de las guías ya existentes con el texto que antes estaba hardcodeado (plantilla "asignatura normal"), para que no rendericen la sección en blanco. El render tolera un dato legado sin exactamente un marcador (lo trata entero como "antes de la tabla") en vez de fallar.

**Limitación real del código: el `DirectorPrograma` no puede editarlo todavía.** La pantalla "Gestionar evaluación" ofrece el área de texto y el botón de guardado también al `DirectorPrograma` (la ruta del frontend es compartida y no distingue el rol), pero `PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion` exige identidad de `Profesor` que imparte la asignatura (`get_current_profesor_id`): sin identidad de `Profesor` responde `403` (`Cuenta sin Profesor asociado`) y, con ella pero sin impartir la asignatura, `404` uniforme -- en ningún caso la guarda. Esto no es la corrección excepcional del resto de la `Guia` (ver [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)): ese guardado propio no se amplió al Director en el issue [#612](https://github.com/mmasias/pyCelda/issues/612) y queda como brecha conocida (nota (c) de [#610](https://github.com/mmasias/pyCelda/issues/610)); `Admin` sigue fuera de alcance.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : editarTextoSistemaEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia{texto_sistema_evaluacion}`
- [Discussion #609](https://github.com/mmasias/pyCelda/discussions/609) -- debate completo de Patrón A vs. B
- [Issue #610](https://github.com/mmasias/pyCelda/issues/610) -- especificación de implementación
