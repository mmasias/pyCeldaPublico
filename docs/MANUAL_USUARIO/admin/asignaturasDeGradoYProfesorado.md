<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Asignaturas de grado y profesorado

## Qué es

Cada asignatura de grado nace de una asignatura del catálogo institucional, adscrita a una materia y a un curso concreto de un grado. Desde aquí se crea, se edita, se da de baja y se le asigna o desasigna profesorado.

## Cómo llegar

La tabla de asignaturas del grado aparece en el detalle del grado (capítulo [Estructura académica](estructuraAcademica.md)), con **Asignatura**, **Materia**, **Curso**, **Carácter**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada una.

## Crear una asignatura de grado

1. Pulsar **+ Crear AsignaturaGrado**.
2. Elegir **Materia** y **Asignatura** (del catálogo institucional -- al elegirla, **Nombre**, **ECTS** y **Contenido** se rellenan con sus valores, editables si difieren).
3. Rellenar **Curso** (1 a 4), **Carácter**, **Idioma**, **Semestre por defecto** y **Sesiones mínimas** (1 a 100: el mínimo de sesiones de planificación docente para poder enviar la guía a revisión).
4. Pulsar **Crear**.

Nombre, ECTS, contenido, idioma y semestre por defecto no vuelven a ser editables desde Admin una vez creada la asignatura de grado.

## Editar una asignatura de grado

Pulsar **Editar** en el detalle. Quedan editables **Materia**, **Curso**, **Carácter** y **Sesiones mínimas**. Si la asignatura ya tiene guías creadas, la **Materia** deja de ser editable y la pantalla lo indica.

## Dar de baja una asignatura de grado

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Esta acción no se puede deshacer: la asignatura de grado pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en ella, pero las guías ya existentes permanecen intactas.

## Profesorado de una asignatura de grado

En el detalle de la asignatura de grado aparece una tabla con el profesorado asignado (**Nombre**, **Email**, y **Quitar** en cada fila), o el aviso de que no tiene ninguno.

### Asignar un profesor

1. Pulsar **Asignar Profesor**.
2. Elegir el profesor en la lista -- solo aparecen los que todavía no imparten esta asignatura de grado.
3. Pulsar **Asignar**.

Si ya está todo el profesorado disponible asignado, la pantalla lo indica y solo ofrece volver atrás.

### Quitar un profesor

Pulsar **Quitar** en su fila. Si es el único profesor asignado, la pantalla advierte de que la asignatura quedará sin profesorado y de que la guía docente que se genere para ella podría quedar incompleta. Pulsar **Confirmar desasignación** para aplicarlo.

---

<sub>

| [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md) | [Índice](README.md) | [Profesores](profesores.md) |
|---|:-:|---|

</sub>
