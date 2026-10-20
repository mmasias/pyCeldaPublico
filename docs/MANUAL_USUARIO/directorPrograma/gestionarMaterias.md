<div align=right>

<sub>[Manual de Director de Programa](README.md)</sub>

</div>

# Gestionar materias

## Qué es

Cada materia agrupa una o más asignaturas del programa. Sobre una materia se asocian o desasocian sus metodologías docentes, sus resultados de aprendizaje y sus competencias, y se reparte su carga de actividades formativas. Si el programa tiene módulos, cada materia puede pertenecer a uno.

## Cómo llegar

Desde la franja del programa, pulsar **📚 Materias**.

## Qué muestra

Una tabla con **Nombre** y el botón **📂 Abrir** de cada materia. Si alguna materia del programa tiene módulo, la tabla se agrupa por módulo: una fila de cabecera **🧱 código -- nombre** por módulo, con sus materias debajo, y al final **🧱 Sin módulo** con las que aún no tienen. Crear, renombrar y eliminar materias, y asignarles su módulo, lo hace el Admin desde su módulo de administración.

## Detalle de una materia

Al abrir una materia, la pestaña **📚 Materias** queda marcada y el título dice **📚 Materias › nombre de la materia**; pulsar **Materias** en ese título vuelve a la lista. Debajo aparecen el **Módulo** de la materia (código y nombre, o "Sin módulo"), sus **ECTS** y su **Código RUCT** si se han importado de la memoria (solo lectura) y, en este orden: las **Asignaturas de esta materia** (Asignatura, Curso, Carácter, con **📂 Abrir** en cada una -- ver el capítulo [Gestionar asignaturas de programa](gestionarAsignaturasDePrograma.md)), las **Metodologías docentes asociadas**, los **Resultados de aprendizaje asociados**, las **Competencias**, las **Actividades formativas de la materia** y, al final, los **Sistemas de evaluación**. El nombre de la materia no se edita aquí (lo hace el Admin); lo que sí se gestiona desde aquí son las secciones siguientes. Admin puede hacer lo mismo desde su vista de la materia: las dos son espejo.

## Metodologías docentes

Tabla con **Código**, **Descripción**, **Descripción propia** (un matiz específico de esta materia sobre la metodología general) y los botones **✏️ Editar** y **➖** (Quitar) de cada fila.

### Asociar una metodología docente

1. Pulsar **➕ Asociar metodología docente**.
2. Elegir la metodología de la lista desplegable -- solo aparecen las del catálogo del programa (pestaña **🧩 Metodologías**) que la materia todavía no tiene.
3. Pulsar **Asociar**.

Si no queda ninguna metodología disponible para asociar, la pantalla lo indica y solo ofrece volver atrás.

### Editar la descripción propia

Pulsar **✏️ Editar** en la fila de la metodología. El código y la descripción general no son editables aquí, solo la **Descripción propia**.

### Quitar una metodología

Pulsar **➖** (Quitar) en la fila de la metodología. Si ninguna asignatura de la materia la está usando, aparece una pantalla de confirmación (**Confirmar desasociación** / **Cancelar**). Si alguna asignatura la está usando, la desasociación queda bloqueada y la pantalla indica en qué asignaturas está en uso -- hace falta quitarla antes de esas asignaturas.

## Resultados de aprendizaje

Misma mecánica que las metodologías docentes: tabla con **Código**, **Tipo**, **Descripción**, **Asignaturas** (el número de asignaturas de la materia que tienen asociado ese resultado; con fondo rojo suave si es 0) y el botón **➖** (Quitar) de cada fila; **➕ Asociar resultado de aprendizaje** para añadir uno de los disponibles. En el desplegable, cada resultado aparece con su código y el comienzo de su texto; el texto completo del elegido se ve debajo. Quitar uno en uso en alguna asignatura de la materia queda bloqueado, con el mismo tipo de aviso.

## Competencias

Misma mecánica que los resultados de aprendizaje: tabla con **Código**, **Tipo**, **Descripción**, **Asignaturas** (cuántas asignaturas de la materia tienen asociada la competencia; con fondo rojo suave si es 0) y **➖** (Quitar); **➕ Asociar competencia** para añadir una de las del programa que la materia aún no tiene. Quitar una que usa alguna asignatura de la materia queda bloqueado. Detalle en el capítulo [Competencias](competencias.md).

## Actividades formativas de la materia

Tabla de solo lectura con **Actividad formativa**, **Horas** y **Presencialidad (%)**: la memoria fija las dos por materia (las asignaturas solo reparten horas). Pulsar **Editar reparto** abre un formulario con los dos campos por actividad (horas mínimo 0, presencialidad de 0 a 100) y el **Total** de horas; si la materia tiene sus ECTS de la memoria, junto al total aparecen las horas que corresponden a 25 h por ECTS y si cuadran. **Guardar** confirma los nuevos valores.

Si la materia tiene ECTS, bajo la tabla una línea compara sus horas con las que corresponden (25 h por ECTS): **OK** o **Discrepancia** con la diferencia. Es informativa: no impide guardar ni reparte nada entre las asignaturas.

Debajo, la tabla **Estado de las actividades formativas** compara, por actividad, las horas de la materia con la suma de las de sus asignaturas: **OK** si cuadran o **Discrepancia** con la diferencia. Es solo informativa: no impide guardar. Si la materia tiene optatividad -- sus asignaturas no suman sus ECTS (idiomas alternativos, optativas, o asignaturas de la memoria que están en otra materia) y la materia sí suma 25 h por ECTS --, esta tabla no aparece: cada asignatura lleva 25 h por ECTS y la suma de sus horas no tiene por qué coincidir con la de la materia. En su lugar, bajo la línea de horas, la pantalla dice "Materia con optatividad: sus asignaturas suman X ECTS para Y de la materia". Que cada asignatura cuadre lo dice entonces su propia línea de horas (capítulo [Gestionar asignaturas de programa](gestionarAsignaturasDePrograma.md)).

## Sistemas de evaluación

Tabla con **Código**, **Tipo**, **Descripción**, **Ponderación mínima** y **Ponderación máxima** de cada sistema, con **✏️ Editar** y **🗑️** (Eliminar) en cada fila. En los títulos cuya memoria publica el RUCT con sistemas por materia, los carga la importación tal como figuran en ella (código, denominación y horquilla); en ese caso conviene no cambiarlos a mano, porque la guía tiene que nombrarlos como la memoria.

- **➕ Crear sistema de evaluación**: el **Código** de la memoria (p. ej. E1, opcional), el **Tipo** (**Evaluación continua** o **Evaluación final**), la **Descripción** (la denominación de la memoria, p. ej. "Prueba Parcial") y las ponderaciones mínima y máxima en porcentaje (0 ≤ mínima ≤ máxima ≤ 100), y pulsar **Crear**.
- **✏️ Editar**: los mismos campos. **Guardar** vuelve a la materia.
- **🗑️**: pide confirmación. Si el sistema se usa en la evaluación de alguna guía, queda bloqueado y la pantalla dice en qué asignaturas.

Crear un sistema o cambiar su rango se rechaza si alguna guía del curso activo **En revisión** o **Aprobada** dejaría de cumplirlo: la suma de sus instrumentos de ese sistema tiene que quedar entre la mínima y la máxima, y un sistema nuevo cuenta como 0 % en las guías que ya existen. El aviso nombra cada asignatura con lo que tiene asignado. Las guías en borrador o rechazadas no cuentan: se vuelven a comprobar al enviarlas a revisión.

---

<div align=center>

| [Entrar y ver los programas](entrarYVerLosProgramas.md) | [Índice](README.md) | [Gestionar asignaturas de programa](gestionarAsignaturasDePrograma.md) |
|---|:-:|---|

</div>
