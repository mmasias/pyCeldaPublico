# editarTextoSistemaEvaluacion()

El texto de convocatorias del apartado 5 de la guía docente sale de una plantilla con dos datos que la personalizan; nadie lo edita ([issue #791](https://github.com/mmasias/pyCelda/issues/791)). Antes ([issue #610](https://github.com/mmasias/pyCelda/issues/610), debate de #609) era texto libre de la `Guia`. Se documenta como ficha propia y no como ampliación de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md): edita otros atributos (`Guia.plantillaEvaluacion`, `instrumentoExtraordinario`, `porcentajeRecuperable`), con endpoint de guardado propio, aunque vive en la pantalla "Gestionar evaluación".

**Actor:** Profesor que imparte la asignatura; el DirectorPrograma que dirige el Programa de la guía también puede, como corrección excepcional ([#612](https://github.com/mmasias/pyCelda/issues/612), [#707](https://github.com/mmasias/pyCelda/issues/707)), con la transición de estado Aprobada -> Borrador / EnRevision -> Rechazada. Admin queda fuera.

**Pantalla:** `PonderacionesEvaluacion` (`/guias/{guiaId}/ponderaciones-evaluacion`): selector de plantilla, instrumento y porcentaje de la convocatoria extraordinaria (si la plantilla los tiene), propuesta a partir de los instrumentos de evaluación final y texto resultante en solo lectura.

**Endpoints:** `GET /api/v1/plantillas-evaluacion` (las cinco plantillas, con su texto) y `PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion`, body `{ plantilla, instrumento_extraordinario, porcentaje_recuperable }`, independiente de `guardarBorradorGuia()`.

## Reglas

- `plantilla` es una de las cinco (asignatura normal, prácticas externas, prácticas de laboratorio, Trabajo Fin de Grado/Máster, recuperación por partes); `porcentaje_recuperable` vacío o entero de 1 a 100; `instrumento_extraordinario` vacío o de una línea de hasta 300 caracteres, sin los marcadores de la plantilla. Si no, 422 sin cambios. Con una plantilla sin campos, los dos se guardan vacíos.
- Sin plantilla elegida se aplica la del carácter de la `AsignaturaPrograma`.
- El texto se compone en el modelo (`Guia.texto_convocatorias`), con "pendiente de concretar" en los campos vacíos; la pantalla, la previsualización y el PDF usan el mismo.
- Regla `c4` de `enviarGuiaARevision()`: con una plantilla que tiene los dos campos, los dos están rellenos.
- Patrón B: `activarCursoAcademico()` clona la plantilla elegida y los dos campos de la `Guia` previa; sin predecesora, la del carácter y los campos vacíos.
- Render: se parte el texto compuesto por `[TABLA]` (antes / tabla de ponderaciones / después). Tras la sección va siempre el párrafo fijo de régimen de uso de IA.
- Migración a esquema versión 6: `migrar_plantilla_evaluacion.py` conserva el porcentaje que se hubiera escrito en el texto libre y retira `texto_sistema_evaluacion`.
