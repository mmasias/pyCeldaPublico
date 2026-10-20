<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Materias y sistemas de evaluación

## Qué es

Cada materia agrupa una o más asignaturas de un programa. Desde Admin se crea la materia, se le asigna su módulo y se gestiona todo su contenido: sistemas de evaluación, resultados de aprendizaje, competencias, metodologías docentes y horas de actividades formativas. El director de programa puede hacer lo mismo en las materias de sus programas: las dos vistas son espejo, para que cualquiera de los dos pueda corregir.

## Cómo llegar

Pulsar la pestaña **📚 Materias** del programa.

## Qué muestra

Una tabla con el **Nombre** de cada materia, el número de **Asignaturas** que tiene y el botón **Abrir**. Si alguna materia del programa tiene módulo, la tabla se agrupa por módulo: una fila de cabecera **🧱 código -- nombre** por módulo y, al final, **🧱 Sin módulo** con las que aún no tienen (los módulos se gestionan en la pestaña **🧱 Módulos**, capítulo [Estructura académica](estructuraAcademica.md)). El botón **🗑️** (Eliminar) aparece desactivado: no está disponible en esta versión.

### Crear una materia

1. Pulsar **➕ Crear materia**.
2. Rellenar **Nombre**.
3. Elegir, si procede, el **Módulo** (por defecto, **Sin módulo**). Si el programa no tiene módulos, el formulario lo indica en lugar del desplegable.
4. Pulsar **Crear**.

Tras crearla, la pantalla pasa directamente a editarla.

## Detalle de una materia

Al abrir una materia aparece, en este orden: sus **Asignaturas** (Asignatura, Curso -- curso en números romanos y semestre por defecto combinados, p. ej. **II-s1** --, Carácter, con acceso a cada una -- capítulo [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md)), sus **Sistemas de evaluación**, sus **Resultados de aprendizaje** (tabla con **Código**, **Tipo**, **Descripción** y **Asignaturas**, el número de asignaturas de la materia en que está asociado cada uno, con fondo rojo suave si es 0), sus **Competencias** (misma tabla), sus **Metodologías docentes** asociadas y las **Actividades formativas de la materia** (ver más abajo). Debajo del nombre, el **Módulo** de la materia (código y nombre, o "Sin módulo") y, si se han importado de la memoria, sus **ECTS** y su **Código RUCT** (solo lectura). Pulsar **Editar** cambia el **Nombre** y el **Módulo** de la materia (**Sin módulo** la saca de su módulo).

## Resultados de aprendizaje, competencias y metodologías docentes

Funcionan igual que para el director de programa (ver su capítulo [Gestionar materias](../directorPrograma/gestionarMaterias.md)):

- **➕ Asociar resultado de aprendizaje**, **➕ Asociar competencia** y **➕ Asociar metodología docente** añaden uno de los disponibles: los del catálogo del programa (sus pestañas, capítulo [Estructura académica](estructuraAcademica.md)) que la materia aún no tiene. En el desplegable, cada resultado o competencia aparece con su código y el comienzo de su texto; el texto completo del elegido se ve debajo.
- **✏️ Editar**, en cada metodología, cambia su **Descripción propia**.
- **➖** (Quitar) retira el resultado, la competencia o la metodología de la materia, con confirmación. Si alguna asignatura de la materia lo está usando, queda bloqueado y la pantalla dice en cuáles.

## Actividades formativas de la materia

La tabla muestra las **Horas** y la **Presencialidad (%)** de cada actividad formativa de la materia: la memoria fija las dos por materia. **Editar reparto** abre un formulario con los dos campos por actividad (horas mínimo 0, presencialidad de 0 a 100) y el total de horas frente a 25 h por ECTS si la materia tiene ECTS; se confirma con **Guardar**. Lo mismo que puede hacer el director de programa.

Si la materia tiene ECTS, bajo la tabla una línea compara sus horas con las que corresponden: **OK** o **Discrepancia**. Es informativa.

Debajo, la tabla **Estado de las actividades formativas** compara, por actividad, las horas de la materia con la suma de las de sus asignaturas: **OK** si cuadran o **Discrepancia** con la diferencia. Es solo informativa: no impide guardar. Si la materia tiene optatividad -- sus asignaturas no suman sus ECTS (idiomas alternativos, optativas, o asignaturas de la memoria que están en otra materia) y la materia sí suma 25 h por ECTS --, esta tabla no aparece: cada asignatura lleva 25 h por ECTS y la suma de sus horas no tiene por qué coincidir con la de la materia. En su lugar, bajo la línea de horas, la pantalla dice "Materia con optatividad: sus asignaturas suman X ECTS para Y de la materia". Que cada asignatura cuadre lo dice entonces su propia línea de horas. Cambiar las horas de la materia no reparte nada entre sus asignaturas; sus horas se editan en cada asignatura (capítulo [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md)).

## Sistemas de evaluación

Pulsar **Abrir sistemas de evaluación** en el detalle de la materia. Aparece una tabla con **Código**, **Tipo**, **Descripción**, **Ponderación** (mínima -- máxima, en porcentaje) y los botones **Abrir** y **🗑️** (Eliminar) de cada sistema. En los títulos cuya memoria publica el RUCT con sistemas por materia, los carga la importación tal como figuran en ella (código, denominación y horquilla); en ese caso conviene no cambiarlos a mano, porque la guía tiene que nombrarlos como la memoria.

### Crear un sistema de evaluación

1. Pulsar **➕ Crear sistema de evaluación**.
2. Escribir, opcionalmente, el **Código** de la memoria (p. ej. E1).
3. Elegir el **Tipo**: **Evaluación continua** o **Evaluación final**.
4. Rellenar la **Descripción**: la denominación del sistema en la memoria (p. ej. "Prueba Parcial"), que es la que nombra la guía.
5. Rellenar **Ponderación mínima** y **Ponderación máxima**, en porcentaje.
6. Pulsar **Crear**.

La ponderación mínima no puede superar la máxima, y ambas deben quedar entre 0 y 100.

### Editar un sistema de evaluación

Pulsar **Editar** en el detalle. Los mismos campos que en el alta quedan editables.

### Rangos que dejarían guías fuera

Crear un sistema o cambiar el rango de uno existente se rechaza si alguna guía del curso activo que está **En revisión** o **Aprobada** dejaría de cumplirlo: la suma de sus instrumentos de ese sistema tiene que quedar entre la ponderación mínima y la máxima, y un sistema nuevo cuenta como 0 % en las guías que ya existen. El aviso dice "El rango deja fuera guías en revisión o aprobadas del curso activo:" seguido de cada asignatura con lo que tiene asignado, por ejemplo **Programación I (40 %)**. Las guías en borrador o rechazadas no cuentan: se vuelven a comprobar al enviarlas a revisión.

### Eliminar un sistema de evaluación

Pulsar **🗑️** (Eliminar) y confirmar en **Confirmar eliminación**. Si el sistema está en uso en la evaluación de alguna guía docente, la eliminación queda bloqueada y la pantalla muestra el aviso "SistemaEvaluacion en uso en:" seguido de los nombres de las asignaturas que lo bloquean -- hace falta retirarlo primero de esas guías.

---

<div align=center>

| [Catálogo de asignaturas](catalogoDeAsignaturasYMetodologias.md) | [Índice](README.md) | [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md) |
|---|:-:|---|

</div>
