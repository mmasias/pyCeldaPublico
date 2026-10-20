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
|**Actor**|`Profesor` (y `DirectorPrograma` como corrección excepcional)|
|**Objetivo**|Elegir la plantilla del texto de convocatorias (apartado 5 de la guía docente) de una `Guia` y concretar su convocatoria extraordinaria|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

El texto de convocatorias **no se edita** (issue [#791](https://github.com/mmasias/pyCelda/issues/791), a petición de Calidad). Se elige una de cinco plantillas y se rellenan los dos datos que la personalizan:

<div align=center>

|Plantilla|Convocatoria extraordinaria|Datos|
|-|-|-|
|Asignatura normal|"...Esta consistirá en [instrumento], con un valor del [porcentaje] % de la nota final de la asignatura..."|instrumento y porcentaje|
|Prácticas de laboratorio|La misma que la asignatura normal|instrumento y porcentaje|
|Prácticas externas|"No aplica"|ninguno|
|Trabajo Fin de Grado/Máster|"TEXTO PENDIENTE": el texto lo tiene que dar Calidad|ninguno|
|Recuperación por partes|"...Esta consistirá en la recuperación de los módulos no superados."|ninguno|

</div>

- **Instrumento**: texto libre de una sola línea (hasta 300 caracteres, sin marcadores entre corchetes como `[TABLA]`), con su artículo: "la prueba de evaluación final (Examen final teórico-práctico)". No se deduce de forma automática: hay asignaturas con dos sistemas finales (pruebas teóricas y prácticas finales en Informática). El sistema propone una redacción con los instrumentos vinculados de los sistemas de tipo "Evaluación final".
- **Porcentaje recuperable**: entero de 1 a 100. El sistema propone la suma de esos mismos instrumentos y avisa, sin bloquear, si el porcentaje no coincide con ella.
- **Plantilla de partida**: mientras nadie elige, se aplica la del carácter de la `AsignaturaPrograma` ("Prácticas Externas" -> prácticas externas; "Trabajo Fin de Grado" -> Trabajo Fin de Grado/Máster; el resto, asignatura normal). Una vez guardada una elección, queda fijada aunque cambie el carácter.
- Con una plantilla sin campos, el instrumento y el porcentaje no se guardan.
- Un campo sin rellenar se lee "pendiente de concretar" en el texto. Con la plantilla normal o la de laboratorio, la guía **no se puede enviar a revisión** hasta que los dos estén rellenos (regla `c4` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md)).

Vive en la pantalla "Gestionar evaluación" (`PONDERACIONES_EVALUACION_ABIERTO`, no un estado propio): una acción más sobre el mismo estado, con endpoint de guardado propio (`PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion`), independiente de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md).

**Patrón B, no Patrón A** (distinción completa en la discussion [#609](https://github.com/mmasias/pyCelda/discussions/609)): la plantilla y sus datos describen la evaluación de **esta** `Guia` y evolucionan curso a curso igual que ella. `activarCursoAcademico()` los clona de la `Guia` anterior; sin predecesora, la plantilla del carácter y los datos sin concretar.

**Corrección excepcional del `DirectorPrograma`** ([#612](https://github.com/mmasias/pyCelda/issues/612), [#707](https://github.com/mmasias/pyCelda/issues/707)): el `DirectorPrograma` que dirige el programa de la `Guia` guarda con el mismo mecanismo que el resto de escrituras sobre la guía (ver [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)): `Aprobada` pasa a `Borrador` y `EnRevision` a `Rechazada`, con fila de `HistorialCambio` con el autor real. Si guarda el `Profesor`, una `Aprobada` vuelve a `Borrador`. `Admin` sigue fuera de alcance, como en el resto de escrituras sobre la guía.

**Antecedente** ([#610](https://github.com/mmasias/pyCelda/issues/610), discussion #609): hasta el esquema versión 6, el texto era dato libre de `Guia` (`texto_sistema_evaluacion`) con tres plantillas de frontend que lo rellenaban sin guardar. En 770 de 775 guías seguía la plantilla normal con los dos huecos "pendiente de concretar" sin rellenar, y la de laboratorio decía "No aplica" en la extraordinaria por error. La migración a la versión 6 conserva el porcentaje de las guías que lo habían escrito y pierde el texto que alguien hubiera editado fuera de los huecos (una guía).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : editarTextoSistemaEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia{plantillaEvaluacion, instrumentoExtraordinario, porcentajeRecuperable}`
- [Issue #791](https://github.com/mmasias/pyCelda/issues/791) -- plantillas, campos y decisiones de Calidad
- [Discussion #609](https://github.com/mmasias/pyCelda/discussions/609) e [issue #610](https://github.com/mmasias/pyCelda/issues/610) -- origen del texto como dato de la `Guia`
