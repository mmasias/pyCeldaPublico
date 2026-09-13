<div align=right>

<sub>[Manual de Director de Grado](README.md)</sub>

</div>

# Gestionar materias

## Qué es

Cada materia agrupa una o más asignaturas del grado. Sobre una materia se asocian o desasocian sus metodologías docentes y sus resultados de aprendizaje, y se reparte su carga de actividades formativas.

## Cómo llegar

Desde la barra de navegación del grado, pulsar **Materias**.

## Qué muestra

Una tabla con **Nombre** y el botón **Abrir** de cada materia. Los botones **Eliminar** (junto a cada fila) y **+ Crear Materia** aparecen desactivados: crear y eliminar materias no está disponible todavía en pyCelda.

## Detalle de una materia

Al abrir una materia aparece, en este orden: las **Asignaturas de esta materia** (Asignatura, Curso, Carácter, con acceso a cada una -- ver el capítulo [Gestionar asignaturas de grado](gestionarAsignaturasDeGrado.md)), las **Metodologías docentes asociadas**, los **Resultados de aprendizaje asociados**, los **Sistemas de evaluación** (catálogo de solo lectura) y las **Actividades formativas de la materia**. El botón **Editar** de la cabecera está desactivado -- los datos propios de la materia (nombre) no son editables todavía; lo que sí se gestiona desde aquí son las cuatro secciones siguientes.

## Metodologías docentes

Tabla con **Código**, **Descripción**, **Descripción propia** (un matiz específico de esta materia sobre la metodología general) y los botones **Editar** y **Quitar** de cada fila.

### Asociar una metodología docente

1. Pulsar **+ Asociar Metodología Docente**.
2. Elegir la metodología de la lista desplegable -- solo aparecen las que la materia todavía no tiene.
3. Pulsar **Asociar**.

Si no queda ninguna metodología disponible para asociar, la pantalla lo indica y solo ofrece volver atrás.

### Editar la descripción propia

Pulsar **Editar** en la fila de la metodología. El código y la descripción general no son editables aquí, solo la **Descripción propia**.

### Quitar una metodología

Pulsar **Quitar** en la fila de la metodología. Si ninguna asignatura de la materia la está usando, aparece una pantalla de confirmación (**Confirmar desasociación** / **Cancelar**). Si alguna asignatura la está usando, la desasociación queda bloqueada y la pantalla indica en qué asignaturas está en uso -- hace falta quitarla antes de esas asignaturas.

## Resultados de aprendizaje

Misma mecánica que las metodologías docentes: tabla con **Código**, **Tipo**, **Descripción** y el botón **Quitar** de cada fila; **+ Asociar Resultado de Aprendizaje** para añadir uno de los disponibles. Quitar uno en uso en alguna asignatura de la materia queda bloqueado, con el mismo tipo de aviso.

## Actividades formativas de la materia

Tabla de solo lectura con **Actividad formativa** y **Horas**. Pulsar **Editar reparto** abre un formulario con un campo de horas por actividad; **Guardar** confirma los nuevos valores.

Si las horas de la materia no coinciden con la suma de las horas de sus asignaturas, aparece debajo una tabla adicional señalando la discrepancia por actividad -- es solo informativa, no impide guardar.

---

<div align=center>

| [Entrar y ver los grados](entrarYVerLosGrados.md) | [Índice](README.md) | [Gestionar asignaturas de grado](gestionarAsignaturasDeGrado.md) |
|---|:-:|---|

</div>
