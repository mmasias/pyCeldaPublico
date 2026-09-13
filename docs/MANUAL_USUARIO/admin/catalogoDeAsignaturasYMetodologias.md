<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Catálogo de asignaturas y metodologías

## Qué es

Dos catálogos institucionales, independientes de cualquier grado concreto: las **asignaturas** (nombre, ECTS y contenido de referencia, del que parte cada asignatura de grado al crearse) y las **metodologías docentes** (código y descripción, asociables luego a las materias).

## Asignaturas

Pulsar **Asignaturas** en el panel de administración. Aparece una tabla con **Nombre**, **ECTS**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada una.

### Crear una asignatura

1. Pulsar **+ Crear Asignatura**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

ECTS y contenido se completan al editar, justo después de crearla.

### Editar una asignatura

Pulsar **Editar** en el detalle de la asignatura. El **Código** no es editable; **Nombre**, **ECTS** y **Contenido** sí.

### Dar de baja una asignatura

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Esta acción no se puede deshacer: la asignatura pasa a estado **Extinguido** y deja de poder usarse en asignaturas de grado nuevas, pero las ya existentes permanecen intactas.

## Metodologías docentes

Pulsar **Metodologías docentes** en el panel de administración. Aparece una tabla con **Código**, **Descripción** y los botones **Abrir** y **Eliminar** de cada una.

### Crear una metodología docente

1. Pulsar **+ Crear Metodología Docente**.
2. Rellenar **Código** y **Descripción**.
3. Pulsar **Crear**.

### Editar una metodología docente

Pulsar **Editar** en el detalle. El **Código** no es editable una vez creada; la **Descripción** sí.

### Eliminar una metodología docente

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Si ninguna materia la tiene asociada, la baja se aplica. Si alguna materia la está usando, la eliminación queda bloqueada y la pantalla lo indica -- esa asociación se retira desde la materia, en la gestión del director de grado, no desde el panel de Admin.
