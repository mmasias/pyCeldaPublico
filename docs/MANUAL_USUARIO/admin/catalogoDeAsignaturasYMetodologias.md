<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Catálogo de asignaturas y metodologías

## Qué es

Tres catálogos institucionales, independientes de cualquier programa concreto: las **asignaturas** (nombre, ECTS y contenido de referencia, del que parte cada asignatura de programa al crearse) las **metodologías docentes** (código y descripción, asociables luego a materias, programas y asignaturas de programa) y las **actividades formativas** (código y nombre, con horas repartidas en materias y asignaturas de programa). Las metodologías y las actividades formativas pertenecen a una universidad.

## Asignaturas

Pulsar **📘 Asignaturas** en el panel de administración. Aparece una tabla con **Nombre**, **Código** (o "--" si todavía no la tiene), **ECTS**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada una.

### Crear una asignatura

1. Pulsar **➕ Crear Asignatura**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

ECTS y contenido se completan al editar, justo después de crearla.

### Editar una asignatura

Pulsar **Editar** en el detalle de la asignatura. El **Código** no es editable; **Nombre**, **ECTS** y **Contenido** sí.

### Dar de baja una asignatura

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Esta acción no se puede deshacer: la asignatura pasa a estado **Extinguido** y deja de poder usarse en asignaturas de programa nuevas, pero las ya existentes permanecen intactas.

### Presente en

Al abrir una asignatura del catálogo, debajo de su detalle aparece la sección **Presente en**: una tabla con cada asignatura de programa que parte de ella (**Programa**, **Materia**, **Curso** -- curso y semestre por defecto tal como los devuelve la asignatura de programa, sin convertir a números romanos -- y **Carácter**), o el aviso "Esta Asignatura no está en ningún Programa todavía" si no la usa ninguna.

## Metodologías docentes

Pulsar **🧩 Metodologías docentes** en el panel de administración. Arriba aparece el selector **Universidad:** (las metodologías listadas son las de la universidad elegida). Aparece una tabla con **Código**, **Descripción** y los botones **Abrir** y **Eliminar** de cada una.

### Crear una metodología docente

1. Pulsar **➕ Crear Metodología Docente** (se crea en la universidad elegida en el selector).
2. Rellenar **Código** y **Descripción**.
3. Pulsar **Crear**.

### Editar una metodología docente

Pulsar **Editar** en el detalle. El **Código** no es editable una vez creada; la **Descripción** sí.

### Eliminar una metodología docente

Pulsar **🗑️ Eliminar** y confirmar en **Confirmar eliminación**. Si ninguna materia, programa ni asignatura de programa la tiene asociada, la baja se aplica. Si está en uso, la eliminación queda bloqueada con el aviso **NO SE PUEDE ELIMINAR** y la lista de dónde está asignada -- hay que retirarla primero de esos sitios (desde el programa o la materia, o desde la asignatura de programa).

## Actividades formativas

Pulsar **🏋️ Actividades formativas** en el panel de administración. Igual que en las metodologías, el selector **Universidad:** elige cuál se lista. Aparece una tabla con **Código**, **Nombre** y los botones **📂 Abrir** y **🗑️ Eliminar** de cada una.

### Crear una actividad formativa

1. Pulsar **➕ Crear Actividad Formativa** (el formulario ofrece **Universidad (*)**, que parte de la elegida en el selector).
2. Rellenar **Código (*)** y **Nombre (*)**.
3. Pulsar **Crear**.

### Editar una actividad formativa

Pulsar **✏️ Editar** en el detalle. El **Código** no es editable una vez creada; el **Nombre** sí.

### Eliminar una actividad formativa

Pulsar **🗑️ Eliminar** y confirmar. Si alguna materia o asignatura de programa tiene horas repartidas en ella, la eliminación queda bloqueada con el aviso **NO SE PUEDE ELIMINAR** y la lista de dónde está asignada; si no, la baja se aplica y no se puede deshacer.

---

<div align=center>

| [Estructura académica](estructuraAcademica.md) | [Índice](README.md) | [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md) |
|---|:-:|---|

</div>
