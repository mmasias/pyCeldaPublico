<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Estructura académica

## Qué es

La jerarquía Universidad -> Facultad -> Programa. Se pueden crear universidades y facultades; editar o eliminar universidades y facultades no está disponible en esta versión. Los programas se gestionan por completo desde aquí: crear, editar el nombre, dar de baja.

## Universidades

Pulsar **Universidades** en el panel de administración. Aparece una tabla con el **Nombre** de cada universidad, el número de **Facultades** que tiene y el botón **Abrir**. El botón **➕ Crear universidad** lleva a un formulario con el **Nombre (*)** de la universidad; se confirma con **Crear** (o **Cancelar**).

Al abrir una universidad aparecen su nombre y una tabla de sus **Facultades** (**Nombre**, número de **Programas** de cada una, **Abrir**). **➕ Crear facultad** lleva a un formulario con el nombre de la facultad, dentro de esa universidad. Los botones **✏️ Editar** de la universidad y la papelera **🗑️** (Eliminar) de cada facultad aparecen desactivados: no están disponibles en esta versión.

## Programas de una facultad

Al abrir una facultad aparece su nombre y una tabla de sus programas, con **Código**, **Nombre**, **Estado** (**Vigente** o **Extinguido**) y los botones **📂 Abrir** y la papelera **🗑️** (Eliminar) de cada uno. El botón **✏️ Editar** de la facultad aparece desactivado, igual que en la universidad.

### Crear un programa

1. Pulsar **➕ Crear programa**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

Tras crearlo, la pantalla pasa directamente a editar el programa recién creado.

## Detalle de un programa

Las pantallas de un programa llevan su nombre en la cabecera y, encima en pequeño, la miga **🏛️ Universidades › universidad › facultad**, cuyos pasos son enlaces para subir en la estructura. Debajo va una franja de pestañas, con la de la pantalla actual marcada (igual que en la vista del director de programa):

- **📋 Ficha**: su **Código** y **Estado**, los directores y una tabla de sus **Asignaturas del programa** -- ver el capítulo [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md). **✏️ Editar**, a la derecha del título **Ficha**, cambia el nombre del programa; el código no es editable una vez creado. Al pie de esa pantalla, en **Zona de riesgo**, está **🗑️ Eliminar** (ver más abajo).
- **🧱 Módulos**: los módulos en que se agrupan las materias del programa (ver más abajo).
- **📚 Materias**: las materias del programa -- capítulo [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md).
- **🎯 Resultados de aprendizaje**: los resultados de aprendizaje del programa (ver más abajo).
- **🧭 Competencias**: las competencias del programa (ver más abajo).
- **🧩 Metodologías**: las metodologías docentes del programa (ver más abajo).
- **🚦 Guías**: el seguimiento de sus guías docentes -- capítulo [Seguimiento de guías](seguimientoDeGuias.md).

Desde el detalle del programa ya no hay un botón **Eliminar**: se llega a él desde **Editar**. Desde el listado de programas de la facultad sigue disponible la papelera **🗑️** (Eliminar) de cada fila.

## Dar de baja un programa

Pulsar **🗑️ Eliminar** en **Zona de riesgo** de la pantalla **Editar** (desactivado si el programa ya está **Extinguido**), o la papelera **🗑️** (Eliminar) en la fila del programa en la facultad, y confirmar en **🗑️ Confirmar eliminación**. Esta acción no se puede deshacer: el programa pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en él, pero todo lo ya existente permanece intacto.

## Metodologías docentes del programa

Pulsar la pestaña **🧩 Metodologías** del programa. Aparece una tabla con **Código** y **Descripción** de las metodologías docentes asociadas al programa, con **➖** (Desasociar) en cada fila. **➕ Asociar metodología docente** permite añadir otra del catálogo institucional (ver [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md)). La pestaña **📋 Ficha** regresa al detalle. El director de programa gestiona lo mismo desde su propia pantalla.

## Resultados de aprendizaje del programa

Pulsar la pestaña **🎯 Resultados de aprendizaje** del programa. Aparece una tabla con **Descripción**, **Tipo**, **Código** y **Nº de Asign.** (el número de asignaturas a las que está asignado cada resultado, o "--" si no consta; con fondo rojo suave si es 0), con **📂 Abrir** y la papelera **🗑️** (Eliminar) en cada fila.

- **➕ Crear resultado de aprendizaje**: formulario con **Código (*)**, **Tipo (*)** y **Descripción (*)**; se confirma con **Crear** y se abre el resultado recién creado.
- **📂 Abrir**: la pestaña **🎯 Resultados de aprendizaje** queda marcada y el título es la miga **🎯 Resultados de aprendizaje › código del resultado** (la primera parte vuelve a la lista). Muestra el tipo y la descripción, el botón **✏️ Editar** (mismos campos que el alta) y la sección **Distribución**: las materias y las asignaturas de programa a las que está asignado, cada una con un enlace a su ficha, o "Sin asignaciones a materias ni a asignaturas del programa". Es la misma pantalla que la del director de programa y la de una competencia.
- En **✏️ Editar**, si el tipo del resultado no está en la lista (por ejemplo, uno cargado desde la memoria verificada del programa), el desplegable lo ofrece también, para que guardar sin tocarlo no lo cambie.
- **🗑️** (Eliminar): si el resultado está asignado a alguna materia o asignatura de programa, la pantalla indica **⛔ No se puede eliminar** y lista dónde está asignado, con un enlace a cada materia o asignatura -- hay que retirarlo primero de ahí. Si no, pide confirmación y la baja no se puede deshacer.

## Competencias del programa

Pulsar la pestaña **🧭 Competencias** del programa. Funciona como los resultados de aprendizaje: tabla con **Descripción**, **Tipo**, **Código** y **Nº de Asign.** (cuántas asignaturas del programa tienen asociada cada competencia; con fondo rojo suave si es 0), con **📂 Abrir** y la papelera **🗑️** (Eliminar) en cada fila.

- **➕ Crear competencia**: formulario con **Código (*)**, **Tipo (*)** (Básica, General, Transversal o Específica) y **Descripción (*)**; se confirma con **Crear**. El código no puede repetirse dentro del programa, sin distinguir mayúsculas y minúsculas: si ya existe, el formulario lo indica y conserva lo escrito.
- **📂 Abrir**: muestra tipo y descripción, **✏️ Editar** (mismos campos que el alta) y la **Distribución**: las materias y las asignaturas de programa que la tienen, cada una con un enlace a su ficha.
- **🗑️** (Eliminar): si la competencia está asociada a alguna materia o asignatura de programa, la pantalla indica **⛔ No se puede eliminar** y lista dónde; si no, pide confirmación y la baja no se puede deshacer.

Las competencias se asocian a las materias y, de las de cada materia, a sus asignaturas, desde la sección **Competencias** de cada una (capítulos [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md) y [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md)). El director de programa gestiona lo mismo desde su vista. Los programas cuya memoria sigue el formato nuevo no tienen competencias: la lista queda vacía y no hace falta hacer nada.

## Módulos del programa

Un módulo agrupa materias del programa. Es opcional: una materia puede no tener módulo, y un programa puede no tener ninguno. Solo Admin los gestiona; el director de programa los ve en su lista de materias, agrupada por módulo.

Pulsar la pestaña **🧱 Módulos** del programa. Aparece una tabla con **Código**, **Nombre**, **Descripción** y **Nº de materias**, con **✏️ Editar** y la papelera **🗑️** (Eliminar) en cada fila.

- **➕ Crear módulo**: formulario con **Código (*)**, **Nombre (*)** y **Descripción** (opcional); se confirma con **Crear** y se vuelve a la lista. El código no puede repetirse dentro del programa, sin distinguir mayúsculas y minúsculas.
- **✏️ Editar**: los mismos campos, con los datos actuales.
- **🗑️** (Eliminar): si el módulo tiene materias, la pantalla lo indica y las lista; hay que cambiarles antes el módulo (editando cada materia). Si no tiene, pide confirmación.

El módulo de cada materia se elige al crearla o editarla, en el desplegable **Módulo** (capítulo [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md)).

## Directores del programa

Junto al **Código** y el **Estado** del programa, la sección **Directores** lista los directores de programa ya nombrados (nombre y email de cada uno) con un botón **➖** (Quitar) en cada fila.

Si queda algún profesor de la universidad sin nombrar, aparece además un selector con esos profesores disponibles y un botón **👑 Nombrar**; si ya todos dirigen el programa, en su lugar se muestra el aviso "No hay profesores disponibles: todos ya dirigen este programa."

Esta gestión también puede hacerse en sentido inverso, desde el detalle del propio profesor -- ver el capítulo [Profesores](profesores.md).

---

<div align=center>

| [Entrar y el panel de administración](entrarYElPanel.md) | [Índice](README.md) | [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md) |
|---|:-:|---|

</div>
