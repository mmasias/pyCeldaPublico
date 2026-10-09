<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Cursos académicos

## Qué es

La pantalla donde se gestionan los cursos académicos de cada universidad: ver los existentes, crear uno nuevo, corregir sus fechas, activarlo (convertirlo en el curso vigente) y fijar su semestre activo. Es el curso vigente el que determina en qué curso nacen las guías docentes.

## Cómo llegar

Pulsar **🗓️ Cursos académicos** en el panel de administración. Para volver al panel, **⚙️ Panel**, arriba a la derecha.

## Qué muestra

Encima de la tabla, el selector **Universidad:** (cada universidad tiene su propio plan de cursos; se preselecciona la primera). La tabla tiene las columnas:

- **Curso**: el curso con formato `AAAA-AAAA` (año de inicio y año de fin).
- **Estado**: **Activo** o **Inactivo**. En cada universidad hay a lo sumo un curso **Activo**.
- **Semestre activo**: **1**, **2** o "--" si no se ha fijado ninguno.
- Dos columnas de botones: **📂 Abrir** (en todas las filas) y **Activar** (solo en las filas elegibles; ver más abajo).

Si se acaba de activar un curso, sobre la tabla aparece un mensaje de confirmación en verde.

## Crear un curso académico

1. Pulsar **➕ Crear curso académico**.
2. Elegir la **Universidad (\*)** (viene preseleccionada si solo hay una) e indicar **Inicio (\*)** y **Fin (\*)**, ambas fechas obligatorias.
3. Pulsar **Crear** (o **Cancelar**).

El curso nace **Inactivo** y sin semestre activo: la propia pantalla lo recuerda ("Estado y semestre activo se gestionan al activar el curso"). Un curso creado no se puede eliminar desde la aplicación.

## Abrir un curso

**📂 Abrir** muestra el detalle del curso: **Inicio**, **Fin**, **Estado** y **Semestre activo**, con los botones **✏️ Editar** y **Activar semestre** a la derecha del título. El título es una miga, **🗓️ Cursos académicos › curso**: pulsar **Cursos académicos** vuelve a la lista.

## Editar un curso

Desde el detalle, **✏️ Editar** permite corregir **Inicio (\*)** y **Fin (\*)** y se confirma con **Guardar** (o **Cancelar**).

La edición queda **bloqueada en cuanto el curso tiene guías asociadas**: la pantalla muestra **⛔ No se puede editar** ("Este curso académico tiene Guías asociadas. Los datos de inicio/fin quedan fijos una vez el curso tiene actividad"). El botón **✏️ Editar** sigue visible; el bloqueo se comprueba al entrar en la pantalla. Un curso recién creado, sin guías, sí se puede corregir.

## Activar un curso

El botón **Activar** solo aparece en las filas elegibles. Es elegible:

- el **último curso creado** de la universidad, si está Inactivo; o
- el **penúltimo**, solo si el último no tiene actividad registrada (ningún cambio en sus guías).

Cualquier otro curso, y el que ya está Activo, no muestra el botón.

Al pulsar **Activar**, la pantalla muestra el curso y avisa: **Esta acción no se puede deshacer.** Se confirma con **Confirmar activación** (o **Cancelar**). Si entretanto el curso dejó de ser elegible, aparece **⛔ No se puede activar** con el motivo.

### Qué implica para las guías

- El curso que estaba Activo pasa a **Inactivo** automáticamente (solo el de la misma universidad).
- Se crea **una guía nueva por cada asignatura de programa activa** de la universidad, con o sin profesorado asignado, en estado **Borrador**.
- Si la asignatura tenía guía en el curso que se desactiva, la nueva se **clona** de ella: copia sus **ponderaciones de evaluación** y su **bibliografía**, y toma su **semestre**, **contenido**, **texto del sistema de evaluación** y **sesiones mínimas**. La **planificación docente** (las sesiones) **no se clona**: cada curso se planifica desde cero.
- Si no tenía guía previa, la nueva nace de los datos propios de la asignatura.
- El profesorado de la guía nueva es el asignado en ese momento a la asignatura, no el del curso anterior.

Al terminar, la pantalla vuelve al listado con el mensaje "Curso Académico AAAA-AAAA activado." y, si lo había, "AAAA-AAAA pasa a Inactivo."

## Activar el semestre

Desde el detalle, **Activar semestre** abre una pantalla con el **Semestre activo actual** y la elección **Nuevo semestre:** (**1** o **2**, preseleccionado el actual). **Guardar** aplica el cambio sin confirmación adicional.

No tiene precondiciones: se puede hacer en cualquier curso, Activo o no.

---

<div align=center>

| [Copias de seguridad](copiasDeSeguridad.md) | [Índice](README.md) | [Auditoría](auditoria.md) |
|---|:-:|---|

</div>
