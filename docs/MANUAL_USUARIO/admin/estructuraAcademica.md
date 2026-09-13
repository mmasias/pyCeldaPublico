<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Estructura académica

## Qué es

La jerarquía Universidad -> Facultad -> Grado. Universidades y facultades son de solo consulta en esta versión; los grados sí se gestionan desde aquí: crear, editar el nombre, dar de baja.

## Universidades

Pulsar **Universidades** en el panel de administración. Aparece una tabla con el **Nombre** de cada universidad y el botón **Abrir**. El botón **+ Crear Universidad** aparece desactivado: no está disponible en esta versión.

Al abrir una universidad aparecen su nombre y una tabla de sus **Facultades** (**Nombre**, **Abrir**). Los botones **Editar** de la universidad, **Eliminar** de cada facultad y **+ Crear Facultad** aparecen desactivados: no están disponibles en esta versión.

## Grados de una facultad

Al abrir una facultad aparece su nombre y una tabla de sus grados, con **Código**, **Nombre**, **Estado** (**Vigente** o **Extinguido**) y los botones **Abrir** y **Eliminar** de cada uno. El botón **Editar** de la facultad aparece desactivado, igual que en la universidad.

### Crear un grado

1. Pulsar **+ Crear Grado**.
2. Rellenar **Código** y **Nombre**.
3. Pulsar **Crear**.

Tras crearlo, la pantalla pasa directamente a editar el grado recién creado.

## Detalle de un grado

Al abrir un grado aparecen su **Código**, **Nombre** y **Estado**, y una tabla de sus **Asignaturas del grado** -- ver el capítulo [Asignaturas de grado y profesorado](asignaturasDeGradoYProfesorado.md). Los botones de la cabecera:

- **Editar**: cambia el nombre del grado. El código no es editable una vez creado.
- **Eliminar**: da de baja el grado (aparece desactivado si ya está **Extinguido**).
- **Ver Materias**: lleva a las materias del grado -- capítulo [Materias y sistemas de evaluación](materiasYSistemasDeEvaluacion.md).
- **Estado del curso actual**: lleva al seguimiento de sus guías docentes -- capítulo [Seguimiento de guías](seguimientoDeGuias.md).

## Dar de baja un grado

Pulsar **Eliminar** y confirmar en **Confirmar eliminación**. Esta acción no se puede deshacer: el grado pasa a estado **Extinguido**, deja de admitir altas nuevas apoyadas en él, pero todo lo ya existente permanece intacto.

---

<sub>

| [Entrar y el panel de administración](entrarYElPanel.md) | [Índice](README.md) | [Catálogo de asignaturas y metodologías](catalogoDeAsignaturasYMetodologias.md) |
|---|:-:|---|

</sub>
