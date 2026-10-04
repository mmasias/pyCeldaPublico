# Estructura del sistema

pyCelda organiza sus datos en dos tipos de relación distintos: una jerarquía donde cada nivel pertenece al anterior (universidad, facultad, programa, materia y lo que cuelga de ella), y catálogos que existen de forma independiente y se asignan donde haga falta (asignaturas, metodologías docentes, resultados de aprendizaje, actividades formativas). Este mapa muestra el conjunto completo y quién gestiona cada bloque, antes de entrar en el detalle de cada tarea en los tres manuales.

## El mapa

![](/images/MANUAL_USUARIO/estructuraDelSistema.svg)

- Flecha continua: el bloque de destino nace y muere con el de origen.
- Flecha discontinua: el bloque de origen es un catálogo independiente, asignado al de destino -- la misma entrada del catálogo puede usarse en varios sitios a la vez.
- Color de cada bloque: quién lo gestiona -- leyenda completa en el propio diagrama.

## Responsables

| Bloque | Quién lo gestiona |
|---|---|
| Universidades y facultades | Admin: crear universidades y facultades y consultarlas; editarlas o eliminarlas todavía no está disponible |
| Programas | Admin: crear, editar el nombre, dar de baja, nombrar o quitar director de programa, y gestionar sus metodologías docentes y sus resultados de aprendizaje; el director de programa gestiona también las de su programa |
| Materias | Admin crea la materia; el director de programa gestiona su contenido -- metodologías docentes, resultados de aprendizaje y actividades formativas asociadas |
| Sistemas de evaluación | Admin |
| Asignaturas de programa | Admin crea, da de baja, asigna el profesorado y edita todos sus campos igual que el director de programa; el director de programa edita el contenido académico -- curso, carácter, idioma, temario, requisitos previos, semestre -- y sus asociaciones de metodologías docentes, resultados de aprendizaje y actividades formativas. Admin tiene la misma paridad de edición y de asociaciones |
| Guías docentes | El profesorado redacta (temario, evaluación, bibliografía, planificación docente); el director de programa decide (aprobar, rechazar, revocar una aprobación, ajustar el semestre) y, como corrección excepcional, puede editar su contenido; Admin supervisa (consulta el estado, previsualiza y descarga el PDF) |
| Catálogo de asignaturas | Admin |
| Catálogo de metodologías docentes | Admin gestiona el catálogo institucional (por universidad); el director de programa elige cuáles se asocian a su programa, a cada materia y, dentro de ella, a cada asignatura de programa |
| Catálogo de resultados de aprendizaje | El director de programa -- creación y reparto en materias y asignaturas de programa; Admin también puede crearlos, editarlos y eliminarlos por programa y asociarlos a asignaturas de programa |
| Catálogo de actividades formativas | Admin gestiona el catálogo (por universidad): crear, editar, eliminar; el director de programa reparte las horas por materia y por asignatura de programa |
