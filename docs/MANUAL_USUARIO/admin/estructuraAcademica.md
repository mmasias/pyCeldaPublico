<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Estructura académica

## Qué es

La jerarquía Universidad -> Facultad -> Programa. Se pueden crear universidades y facultades; editar o eliminar universidades y facultades no está disponible en esta versión. Los programas se gestionan por completo desde aquí: crear, editar el nombre, dar de baja.

## Universidades

Pulsar **Universidades** en el panel de administración. Aparece una tabla con el **Nombre** de cada universidad, el número de **Facultades** que tiene y el botón **Abrir**. El botón **➕ Crear Universidad** lleva a un formulario con el **Nombre (*)** de la universidad; se confirma con **Crear** (o **Cancelar**).

Al abrir una universidad aparecen su nombre y una tabla de sus **Facultades** (**Nombre**, número de **Programas** de cada una, **Abrir**). **➕ Crear Facultad** lleva a un formulario con el nombre de la facultad, dentro de esa universidad. Los botones **✏️ Editar** de la universidad y **🗑️ Eliminar** de cada facultad aparecen desactivados: no están disponibles en esta versión.

## Programas de una facultad

Al abrir una facultad aparece su nombre y una tabla de sus programas, con **Código**, **Nombre**, **Estado** (**Vigente** o **Extinguido**) y los botones **📂 Abrir** y **🗑️ Eliminar** de cada uno. El botón **✏️ Editar** de la facultad aparece desactivado, igual que en la universidad.

### Crear un programa

1. Pulsar **➕ Crear Programa**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

Tras crearlo, la pantalla pasa directamente a editar el programa recién creado.

## Detalle de un programa

Al abrir un programa aparecen su **Código**, **Nombre** y **Estado**, y una tabla de sus **Asignaturas del programa** -- ver el capítulo [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md). Los botones de la cabecera:

- **✏️ Editar**: cambia el nombre del programa. El código no es editable una vez creado. Al pie de esa pantalla, en **Zona de riesgo**, está **🗑️ Eliminar** (ver más abajo).
- **📚 Ver Materias**: lleva a las materias del programa -- capítulo [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md).
- **🧩 Ver Metodologías**: lleva a las metodologías docentes del programa (ver más abajo).
- **🎯 Resultados de Aprendizaje**: lleva a los resultados de aprendizaje del programa (ver más abajo).
- **🚦 Estado del curso actual**: lleva al seguimiento de sus guías docentes -- capítulo [Seguimiento de guías](seguimientoDeGuias.md).

Desde el detalle del programa ya no hay un botón **Eliminar**: se llega a él desde **Editar**. Desde el listado de programas de la facultad sigue disponible el botón **🗑️ Eliminar** de cada fila.

## Dar de baja un programa

Pulsar **🗑️ Eliminar** (en **Zona de riesgo** de la pantalla **Editar**, o en la fila del programa en la facultad; aparece desactivado si el programa ya está **Extinguido**) y confirmar en **🗑️ Confirmar eliminación**. Esta acción no se puede deshacer: el programa pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en él, pero todo lo ya existente permanece intacto.

## Metodologías docentes del programa

Pulsar **🧩 Ver Metodologías** en el detalle del programa. Aparece una tabla con **Código** y **Descripción** de las metodologías docentes asociadas al programa, con **➖ Desasociar** en cada fila. **➕ Asociar Metodología Docente** permite añadir otra del catálogo institucional (ver [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md)). **Volver al Programa** regresa al detalle. Es la misma pantalla que tiene el director de programa.

## Resultados de aprendizaje del programa

Pulsar **🎯 Resultados de Aprendizaje** en el detalle del programa. Aparece una tabla con **Descripción**, **Tipo**, **Código** y **Nº de Asign.** (el número de asignaturas a las que está asignado cada resultado, o "--" si no consta), con **📂 Abrir** y **🗑️ Eliminar** en cada fila.

- **➕ Crear Resultado de Aprendizaje**: formulario con **Código (*)**, **Tipo (*)** y **Descripción (*)**; se confirma con **Crear**.
- **📂 Abrir**: muestra código, tipo y descripción, el botón **✏️ Editar** (mismos campos que el alta) y la sección **Distribución**: las materias y las asignaturas de programa a las que está asignado, o "Sin asignaciones a materias ni asignaturas-programa".
- **🗑️ Eliminar**: si el resultado está asignado a alguna materia o asignatura de programa, la pantalla indica **NO SE PUEDE ELIMINAR** y lista dónde está asignado -- hay que retirarlo primero de ahí. Si no, pide confirmación y la baja no se puede deshacer.

## Directores del programa

Junto al **Código** y el **Estado** del programa, la sección **Directores** lista los directores de programa ya nombrados (nombre y email de cada uno) con un botón **➖ Quitar** en cada fila.

Si queda algún profesor de la universidad sin nombrar, aparece además un selector con esos profesores disponibles y un botón **👑 Nombrar**; si ya todos dirigen el programa, en su lugar se muestra el aviso "No hay Profesores disponibles: todos ya dirigen este Programa."

Esta gestión también puede hacerse en sentido inverso, desde el detalle del propio profesor -- ver el capítulo [Profesores](profesores.md).

---

<div align=center>

| [Entrar y el panel de administración](entrarYElPanel.md) | [Índice](README.md) | [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md) |
|---|:-:|---|

</div>
