<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Entrar y el panel de administración

## Entrar

El acceso de Admin tiene una dirección propia, separada de la del profesorado y los directores de programa. Pulsar **🔑 Iniciar sesión** y autenticarse con Google con una cuenta con permisos de Admin. Al pie de esa pantalla, en pequeño, se ve la versión de la aplicación y la versión de esquema de la base de datos (p. ej. `Versión v0.11.8 · esquema 2`).

## El panel de administración

Tras entrar aparece el panel de administración, con un botón por cada bloque de gestión, en dos grupos:

- **Estructura y catálogos**: **🏛️ Universidades**, **📘 Asignaturas**, **🧩 Metodologías docentes**, **🏋️ Actividades formativas**, **🧑‍🏫 Profesores** y **🗓️ Cursos académicos** ([capítulo](cursosAcademicos.md)).
- **Sistema**: **💾 Copias de seguridad**, **🔍 Auditoría** ([capítulo](auditoria.md)) y **📄 Generar guías PDF**.

Los bloques de gestión llevan al capítulo correspondiente de este manual. Los programas y sus materias no tienen botón propio en el panel: se llega a ellos entrando primero en una universidad y su facultad (capítulo [Estructura académica](estructuraAcademica.md)).

**📄 Generar guías PDF** aparece desactivado: no está disponible en esta versión.

Todas las pantallas de Admin llevan una **barra azul** fija en el borde superior de la ventana: es la señal de que se está en modo Admin y no en el modo académico del profesorado y los directores.

**🚪 Cerrar sesión**, arriba a la derecha, vuelve a la pantalla de entrada.

En las demás pantallas de Admin que no son formularios, arriba a la derecha están siempre **⚙️ Panel**, que vuelve a este panel, y **🚪 Cerrar sesión**, separado debajo. Los formularios no los llevan: se sale con **Guardar** o **Cancelar**. En los formularios de crear y editar, si se ha escrito o cambiado algo, **Cancelar** pregunta "Tienes cambios sin guardar. ¿Salir sin guardarlos?" antes de descartarlo. En los formularios largos (crear y editar asignatura del programa, sus actividades formativas) aparece también un **Guardar** (o **Crear**) arriba en cuanto hay cambios, con el aviso "Tienes cambios sin guardar.".

La sesión dura 12 horas. Si al guardar en un formulario (crear o editar, asociar, asignar profesor, definir director, activar semestre) o al crear una copia de seguridad con su motivo la sesión ha caducado, el formulario no se cierra ni se pierde lo escrito: aparece "⚠️ Tu sesión ha caducado. No pierdes lo escrito: entra de nuevo en otra pestaña y, al volver aquí, repite la acción." El enlace abre la entrada de Admin en una pestaña nueva; tras entrar, se vuelve a la pestaña del formulario y se pulsa otra vez el botón. En los formularios largos (asignatura del programa, sus actividades formativas) el aviso sale también junto a **Guardar**. Hay que entrar por el enlace del aviso, que es la entrada de Admin: si se entra por la del profesorado, la sesión deja de ser de Admin, el siguiente guardado lleva a la entrada de Admin y lo escrito sí se pierde.

Las fichas (un profesor, una asignatura, una materia, una universidad...) no tienen botón "Volver a...": su título es una **miga** con el camino desde el listado, por ejemplo **🧑‍🏫 Profesores › Ana García** o **🏛️ Universidades › UNEATLANTICO › Facultad de Ingeniería**. Cada paso de la miga es un enlace a su pantalla; un nombre largo aparece recortado y se ve completo al pasar el ratón. Las acciones de la ficha (**✏️ Editar**, **➕ Crear**...) van a la derecha de la miga.

---

<div align=center>

|  | [Índice](README.md) | [Estructura académica](estructuraAcademica.md) |
|---|:-:|---|

</div>
