<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Estructura académica

## Qué es

La jerarquía Universidad -> Facultad -> Programa. Universidades y facultades son de solo consulta en esta versión; los programas sí se gestionan desde aquí: crear, editar el nombre, dar de baja.

## Universidades

Pulsar **Universidades** en el panel de administración. Aparece una tabla con el **Nombre** de cada universidad, el número de **Facultades** que tiene y el botón **Abrir**. El botón **+ Crear Universidad** aparece desactivado: no está disponible en esta versión.

Al abrir una universidad aparecen su nombre y una tabla de sus **Facultades** (**Nombre**, número de **Programas** de cada una, **Abrir**). Los botones **Editar** de la universidad, **Eliminar** de cada facultad y **+ Crear Facultad** aparecen desactivados: no están disponibles en esta versión.

## Programas de una facultad

Al abrir una facultad aparece su nombre y una tabla de sus programas, con **Código**, **Nombre**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada uno. El botón **Editar** de la facultad aparece desactivado, igual que en la universidad.

### Crear un programa

1. Pulsar **+ Crear Programa**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

Tras crearlo, la pantalla pasa directamente a editar el programa recién creado.

## Detalle de un programa

Al abrir un programa aparecen su **Código**, **Nombre** y **Estado**, y una tabla de sus **Asignaturas del programa** -- ver el capítulo [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md). Los botones de la cabecera:

- **Editar**: cambia el nombre del programa. El código no es editable una vez creado.
- **Eliminar**: da de baja el programa (aparece desactivado si ya está **Extinguido**).
- **Ver Materias**: lleva a las materias del programa -- capítulo [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md).
- **Estado del curso actual**: lleva al seguimiento de sus guías docentes -- capítulo [Seguimiento de guías](seguimientoDeGuias.md).

## Dar de baja un programa

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Esta acción no se puede deshacer: el programa pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en él, pero todo lo ya existente permanece intacto.

## Directores del programa

Debajo de las asignaturas del programa, la sección **Directores** lista los directores de programa ya nombrados (nombre y email de cada uno) con un botón **Quitar** en cada fila.

Si queda algún profesor de la universidad sin nombrar, aparece además un selector con esos profesores disponibles y un botón **Nombrar**; si ya todos dirigen el programa, en su lugar se muestra el aviso "No hay Profesores disponibles: todos ya dirigen este Programa."

Esta gestión también puede hacerse en sentido inverso, desde el detalle del propio profesor -- ver el capítulo [Profesores](profesores.md).

---

<div align=center>

| [Entrar y el panel de administración](entrarYElPanel.md) | [Índice](README.md) | [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md) |
|---|:-:|---|

</div>
