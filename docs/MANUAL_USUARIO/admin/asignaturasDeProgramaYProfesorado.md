<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Asignaturas de programa y profesorado

## Qué es

Cada asignatura de programa nace de una asignatura del catálogo institucional, adscrita a una materia y a un curso concreto de un programa. Desde aquí se crea, se edita, se da de baja y se le asigna o desasigna profesorado.

## Cómo llegar

La tabla de asignaturas del programa aparece en el detalle del programa (capítulo [Estructura académica](estructuraAcademica.md)), con **Asignatura**, **Materia**, **Curso** (curso en números romanos y semestre por defecto combinados, p. ej. **II-s1**), **Carácter**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **🗑️** (Eliminar) de cada una.

## Crear una asignatura de programa

1. Pulsar **➕ Crear asignatura del programa**.
2. Elegir **Materia** y **Asignatura** (del catálogo institucional -- al elegirla, **Nombre**, **ECTS** y **Contenido** se rellenan con sus valores, editables si difieren).
3. Rellenar **Curso** (1 a 4), **Carácter**, **Idioma**, **Semestre por defecto** y **Sesiones mínimas** (0 a 100: el mínimo de sesiones de planificación docente para poder enviar la guía a revisión; 0 si la asignatura no tiene sesiones, como el TFG).
4. Pulsar **Crear**.


## Editar una asignatura de programa

Pulsar **✏️ Editar** en el detalle. El Admin tiene los mismos campos editables que el director de programa: **Materia**, **Curso**, **Carácter**, **Sesiones mínimas**, **Idioma**, **Semestre por defecto**, **Nombre**, **ECTS**, **Contenido** (hasta 10.000 caracteres) y **Requisitos previos**. Se confirma con **Guardar**.

Las **Sesiones mínimas** se aplican al momento a todas las guías de la asignatura, en cualquier estado: cada guía usa siempre el mínimo vigente de su asignatura. Se comprueba al enviar la guía a revisión, así que una guía que ya está en revisión o aprobada no se ve afectada hasta que vuelva a enviarse. El director de programa también puede cambiarlas desde su pantalla de edición.

Si ya existen guías creadas para la asignatura, la **Materia** y el **Semestre por defecto** dejan de ser editables y la pantalla lo indica.

Tampoco se puede cambiar la asignatura a una materia que no tenga todas sus competencias: el sistema rechaza el cambio y dice qué competencias de la asignatura faltan en la nueva materia. Hay que asociarlas antes a esa materia o quitarlas de la asignatura.

## Dar de baja una asignatura de programa

Pulsar **🗑️** (Eliminar) y confirmar en **🗑️ Confirmar eliminación**. Esta acción no se puede deshacer: la asignatura de programa pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en ella, pero las guías ya existentes permanecen intactas.

## Detalle de una asignatura de programa

Al abrir una asignatura de programa aparecen **Materia**, **Curso**, **Carácter**, **Sesiones mínimas para enviar a revisión**, **Idioma**, **ECTS**, **Semestre por defecto**, **Contenido** y **Requisitos previos**, y debajo estas secciones, en este orden: **Profesorado**, **Resultados de aprendizaje asociados**, **Competencias**, **Metodologías docentes asociadas** y **Actividades formativas**. Arriba, la franja del programa con **📚 Materias** marcada y, debajo, la miga **📚 Materias › materia › asignatura**: cada paso vuelve a su pantalla; la ficha del programa con su tabla de asignaturas está en la pestaña **📋 Ficha**.

## Resultados de aprendizaje asociados

La tabla muestra **Código**, **Tipo** y **Descripción** de cada resultado asociado, con **➖** (Quitar) en cada fila.

Para añadir uno, pulsar **➕ Asociar resultado de aprendizaje**, elegirlo en **Resultado de aprendizaje (*)** y confirmar. En el desplegable, cada resultado aparece con su código y el comienzo de su texto; el texto completo del elegido se ve debajo. Solo se ofrecen los resultados ya asignados a la materia de la asignatura de programa y que aún no están asociados a ella; si no queda ninguno, la pantalla lo indica y solo ofrece **Volver**.

## Competencias

Tabla con **Código**, **Tipo** y **Descripción** de cada competencia asociada, con **➖** (Quitar) en cada fila; quitar pide confirmación. **➕ Asociar competencia** añade una: solo se ofrecen las ya asociadas a la materia de la asignatura y que esta aún no tiene; si no queda ninguna, la pantalla lo indica. Las competencias de la asignatura aparecen también, en solo lectura, en su guía docente.

## Metodologías docentes asociadas

La tabla muestra **Código** y **Descripción**, con **➖** (Quitar) en cada fila. **➕ Asociar metodología docente** añade otra, elegida de las disponibles (si no queda ninguna, la pantalla lo indica). Al quitar la última metodología asociada, la pantalla advierte **Sin metodologías docentes tras esta acción**: la guía docente que se genere para esa asignatura podría quedar incompleta.

## Actividades formativas

La tabla muestra, por cada actividad formativa, las **Horas** y el **% presencialidad**, que es el de la materia (se edita en la materia). **Editar reparto** abre un formulario con las **Horas** de cada actividad (mínimo 0) y se confirma con **Guardar**.

Si la asignatura tiene ECTS, bajo la tabla una línea compara sus horas con las que corresponden (25 h por ECTS): **OK** o **Discrepancia** con la diferencia, o "sin horas de actividades formativas" si aún no tiene. La misma línea aparece en el formulario de **Editar reparto** y se actualiza mientras se escriben las horas. Es informativa: no impide guardar.

## Profesorado de una asignatura de programa

En el detalle de la asignatura de programa aparece una tabla con el profesorado asignado (**Profesor**: su nombre o, si no lo tiene registrado, su email; las casillas **Responsable** e **Imparte**; y **➖** (Quitar) en cada fila), o el aviso de que no tiene ninguno.

Cada profesor asignado es **responsable** de la asignatura, la **imparte** o ambas cosas. Los dos papeles pueden editar la guía por igual; la diferencia está en el PDF: en **DOCENTE** y **EMAIL** de la guía docente (y en **DOCENTE** de la planificación docente) solo aparece quien la imparte. En la guía dentro de la aplicación se ven los dos papeles junto a cada nombre.

Una asignatura con profesorado tiene que tener siempre al menos un profesor que la imparta. Quedarse sin profesorado sí está permitido.

**Efecto sobre la guía del curso activo.** Solo cambia la guía lo que cambia quién la imparte, porque es lo único que sale en el PDF. Si la guía estaba **Aprobada** y se asigna o se quita a un profesor que la imparte, o se le pone o quita **Imparte** a alguien, la guía pasa a **En revisión** para que el director la vuelva a aprobar. Asignar o quitar a alguien que solo es responsable, o cambiar solo **Responsable**, no cambia el estado de la guía.

### Asignar un profesor

1. Pulsar **Asignar profesor** (en la sección **Profesorado**).
2. Elegir el profesor en la lista -- solo aparecen los que todavía no están asignados a esta asignatura de programa.
3. Marcar su papel: **Responsable**, **Imparte** o los dos (por defecto, solo **Imparte**: **Responsable** se marca a propósito). Hay que marcar al menos uno.
4. Pulsar **Asignar**.

Si nadie imparte todavía la asignatura, el primer profesor que se asigne tiene que llevar **Imparte**: si no, el sistema rechaza la asignación.

Si ya está todo el profesorado disponible asignado, la pantalla lo indica y solo ofrece volver atrás.

### Cambiar el papel de un profesor

Marcar o desmarcar **Responsable** o **Imparte** en su fila de la tabla: el cambio se guarda al momento. No se puede dejar a un profesor sin ningún papel (para eso está **➖** Quitar), ni quitar **Imparte** al único que la imparte: primero hay que marcar a otro. Si cambia **Imparte** y la guía del curso activo estaba **Aprobada**, pasa a **En revisión** para que el director la vuelva a aprobar; si solo cambia **Responsable**, la guía no cambia de estado.

### Quitar un profesor

Pulsar **➖** (Quitar) en su fila. La pantalla dice que el profesor "deja de impartir" la asignatura o, si solo es responsable, que "deja de estar asignado/a". Si es el único profesor asignado, advierte de que la asignatura quedará sin profesorado y de que la guía docente que se genere para ella podría quedar incompleta. Pulsar **Confirmar desasignación** para aplicarlo.

Si es el único que imparte y quedan otros profesores asignados (solo responsables), la pantalla no ofrece confirmar: explica que no se puede desasignar y solo ofrece **Volver**. Antes hay que marcar **Imparte** a otro profesor o quitar a los responsables.

---

<div align=center>

| [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md) | [Índice](README.md) | [Profesores](profesores.md) |
|---|:-:|---|

</div>
