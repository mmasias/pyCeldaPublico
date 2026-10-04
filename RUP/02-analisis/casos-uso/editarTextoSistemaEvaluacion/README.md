# editarTextoSistemaEvaluacion()

Hallazgo de [issue #610](https://github.com/mmasias/pyCelda/issues/610) (debate de #609): el texto de convocatorias del apartado 5 de la guía docente pasa de estar hardcodeado en la plantilla a ser dato editable de la `Guia`. Se documenta como ficha propia y no como ampliación de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md): edita otro atributo (`Guia.texto_sistema_evaluacion`), con endpoint de guardado propio, aunque vive en la pantalla "Gestionar evaluación".

**Actor:** Profesor que imparte la asignatura (Admin y Director quedan fuera hasta [#601](https://github.com/mmasias/pyCelda/issues/601)).

**Pantalla:** `PonderacionesEvaluacion` (`/guias/{guiaId}/ponderaciones-evaluacion`), `<textarea>` + tres plantillas de frontend (asignatura normal, prácticas externas, prácticas de laboratorio) que rellenan sin guardar.

**Endpoint:** `PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion`, body `{ texto }`, independiente de `guardarBorradorGuia()`.

## Reglas

- `texto` contiene el marcador `[TABLA]` exactamente una vez (422 si 0 o 2+), en cada guardado.
- Patrón B: `Guia.texto_sistema_evaluacion` se clona de la `Guia` previa en `activarCursoAcademico()`; sin predecesora nace vacío.
- Render: se parte por `[TABLA]` (antes / tabla de ponderaciones / después); un dato legado sin exactamente un marcador se pinta entero como "antes", sin fallar. Tras la sección va siempre el párrafo fijo de régimen de uso de IA.
- Migración: `migrar_texto_sistema_evaluacion.py` hace backfill con el texto de "asignatura normal" en las guías existentes.
