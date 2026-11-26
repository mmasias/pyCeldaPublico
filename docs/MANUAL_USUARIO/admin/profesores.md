<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Profesores

## Qué es

El alta, edición y baja del profesorado, y el nombramiento o cese de directores de programa.

## Cómo llegar

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/wireframe.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/abrirProfesores.md)</sub>

</div>

Pulsar **Profesores** en el panel de administración. Aparece una tabla con cada profesor (su nombre o, si aún no lo tiene registrado, su email), el número de asignaturas de programa que tiene asignadas, y los botones [**Abrir**](profesores.md#detalle-de-un-profesor) y [**🗑️**](profesores.md#dar-de-baja-un-profesor) (Eliminar).

## Crear un profesor

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/wireframe.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/crearProfesor.md)</sub>

</div>

1. Pulsar **➕ Crear profesor**.
2. Rellenar **Nombre** y **Email**.
3. Pulsar **Crear**.

## Editar un profesor

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/wireframe.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/editarProfesor.md)</sub>

</div>

Pulsar **Editar** en su detalle. **Nombre** y **Email** son ambos editables.

## Detalle de un profesor

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/wireframe.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/abrirProfesor.md)</sub>

</div>

Muestra las **Asignaturas asignadas** (asignatura y programa de cada una) y los **Programas que dirige**, con el botón **➖** (Quitar) en cada uno para cesarlo como director.

### Nombrar director de programa

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/wireframe.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/definirDirectorPrograma.md)</sub>

</div>

1. Pulsar **👑 Nombrar director de programa**.
2. Elegir el programa en la lista -- solo aparecen los que el profesor todavía no dirige.
3. Pulsar **Nombrar**.

Si ya dirige todos los programas existentes, la pantalla lo indica y solo ofrece volver atrás.

## Dar de baja un profesor

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/wireframe-confirmacion.svg)
|:-:
<sub>[Ver la pantalla en el prototipo navegable](/docs/PROPUESTA_WIREFRAME/admin/eliminarProfesor.md)</sub>

</div>

Pulsar **🗑️** (Eliminar) y confirmar en **Confirmar eliminación**. Si el profesor tiene asignaturas de programa asignadas o dirige algún programa, la baja queda bloqueada y la pantalla lo indica -- hace falta desasignarlo de esas asignaturas y cesarlo como director antes de eliminarlo.

---

<div align=center>

| [Asignaturas de programa y profesorado](asignaturasDeProgramaYProfesorado.md) | [Índice](README.md) | [Seguimiento de guías](seguimientoDeGuias.md) |
|---|:-:|---|

</div>
