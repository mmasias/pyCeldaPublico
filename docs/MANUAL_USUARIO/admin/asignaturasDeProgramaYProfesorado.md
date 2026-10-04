<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Asignaturas de programa y profesorado

## Qué es

Cada asignatura de programa nace de una asignatura del catálogo institucional, adscrita a una materia y a un curso concreto de un programa. Desde aquí se crea, se edita, se da de baja y se le asigna o desasigna profesorado.

## Cómo llegar

La tabla de asignaturas del programa aparece en el detalle del programa (capítulo [Estructura académica](estructuraAcademica.md)), con **Asignatura**, **Materia**, **Curso** (curso en números romanos y semestre por defecto combinados, p. ej. **II-s1**), **Carácter**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada una.

## Crear una asignatura de programa

1. Pulsar **➕ Crear Asignatura del Programa**.
2. Elegir **Materia** y **Asignatura** (del catálogo institucional -- al elegirla, **Nombre**, **ECTS** y **Contenido** se rellenan con sus valores, editables si difieren).
3. Rellenar **Curso** (1 a 4), **Carácter**, **Idioma**, **Semestre por defecto** y **Sesiones mínimas** (1 a 100: el mínimo de sesiones de planificación docente para poder enviar la guía a revisión).
4. Pulsar **Crear**.


## Editar una asignatura de programa

Pulsar **✏️ Editar** en el detalle. El Admin tiene los mismos campos editables que el director de programa: **Materia**, **Curso**, **Carácter**, **Sesiones mínimas**, **Idioma**, **Semestre por defecto**, **Nombre**, **ECTS**, **Contenido** (hasta 10.000 caracteres) y **Requisitos previos**. Se confirma con **Guardar**.

Si ya existen guías creadas para la asignatura, la **Materia** y el **Semestre por defecto** dejan de ser editables y la pantalla lo indica.

## Dar de baja una asignatura de programa

Pulsar **Eliminar** y confirmar en **🗑️ Confirmar eliminación**. Esta acción no se puede deshacer: la asignatura de programa pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en ella, pero las guías ya existentes permanecen intactas.

## Detalle de una asignatura de programa

Al abrir una asignatura de programa aparecen **Materia**, **Curso**, **Carácter**, **Sesiones mínimas para enviar a revisión**, **Idioma**, **ECTS**, **Semestre por defecto**, **Contenido** y **Requisitos previos**, y debajo estas secciones, en este orden: **Profesorado**, **Resultados de aprendizaje asociados**, **Metodologías docentes asociadas** y **Actividades formativas**. Arriba, **Volver al Programa** y **Volver a la Materia**.

## Resultados de aprendizaje asociados

La tabla muestra **Código**, **Tipo** y **Descripción** de cada resultado asociado, con **➖ Quitar** en cada fila.

Para añadir uno, pulsar **➕ Asociar Resultado de Aprendizaje**, elegirlo en **Resultado de aprendizaje (*)** y confirmar. Solo se ofrecen los resultados ya asignados a la materia de la asignatura de programa y que aún no están asociados a ella; si no queda ninguno, la pantalla lo indica y solo ofrece **Volver**.

## Metodologías docentes asociadas

La tabla muestra **Código** y **Descripción**, con **➖ Quitar** en cada fila. **➕ Asociar Metodología Docente** añade otra, elegida de las disponibles (si no queda ninguna, la pantalla lo indica). Al quitar la última metodología asociada, la pantalla advierte **Sin metodologías docentes tras esta acción**: la guía docente que se genere para esa asignatura podría quedar incompleta.

## Actividades formativas

La tabla muestra, por cada actividad formativa, las **Horas** y el **% presencialidad**. **Editar reparto** abre un formulario con una fila por actividad (**Horas**, mínimo 0, y **% presencialidad**, de 0 a 100) y se confirma con **Guardar**.

## Profesorado de una asignatura de programa

En el detalle de la asignatura de programa aparece una tabla con el profesorado asignado (**Nombre**, **Email**, y **Quitar** en cada fila), o el aviso de que no tiene ninguno.

### Asignar un profesor

1. Pulsar **Asignar Profesor** (en la sección **Profesorado**).
2. Elegir el profesor en la lista -- solo aparecen los que todavía no imparten esta asignatura de programa.
3. Pulsar **Asignar**.

Si ya está todo el profesorado disponible asignado, la pantalla lo indica y solo ofrece volver atrás.

### Quitar un profesor

Pulsar **Quitar** en su fila. Si es el único profesor asignado, la pantalla advierte de que la asignatura quedará sin profesorado y de que la guía docente que se genere para ella podría quedar incompleta. Pulsar **Confirmar desasignación** para aplicarlo.

---

<div align=center>

| [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md) | [Índice](README.md) | [Profesores](profesores.md) |
|---|:-:|---|

</div>
