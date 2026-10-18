<div align=right>
  
  <sub>Volver: [Al inicio](/README.md) / Manuales: [Profesor](profesor/README.md) · [Director de Programa](directorPrograma/README.md) · [Administrador](admin/README.md)</sub>
</div>

pyCelda organiza sus datos en dos tipos de relación distintos: una jerarquía donde cada nivel pertenece al anterior (universidad, facultad, programa, materia y lo que cuelga de ella, más los cursos académicos y el profesorado de cada universidad), y catálogos que existen de forma independiente y se asignan donde haga falta (asignaturas, metodologías docentes, resultados de aprendizaje, actividades formativas; y los profesores, que se asignan a asignaturas de programa y pueden dirigir un programa). Este mapa muestra el conjunto completo y quién gestiona cada bloque, antes de entrar en el detalle de cada tarea en los tres manuales.

## El mapa

![](/images/MANUAL_USUARIO/estructuraDelSistema.svg)

- Flecha continua: el bloque de destino nace y muere con el de origen.
- Flecha discontinua: el bloque de origen es un catálogo independiente, asignado al de destino -- la misma entrada del catálogo puede usarse en varios sitios a la vez.
- Color de cada bloque: quién lo gestiona -- leyenda completa en el propio diagrama.

## Responsables

| Bloque | Quién lo gestiona |
|---|---|
| Universidades y facultades | Admin: crear universidades y facultades y consultarlas; editarlas o eliminarlas todavía no está disponible |
| Programas | Admin: crear, editar el nombre, dar de baja, nombrar o quitar director de programa, y gestionar sus catálogos de metodologías docentes, actividades formativas, resultados de aprendizaje y competencias, y sus módulos; el director de programa gestiona también los cuatro catálogos de su programa (los módulos, solo Admin). El código RUCT y la denominación oficial del programa los carga la importación desde el RUCT |
| Módulos | Admin: crear, editar y eliminar los módulos de cada programa, y elegir el módulo de cada materia al crearla o editarla; el director de programa los ve agrupando su lista de materias. Un módulo agrupa materias de su programa; es opcional para cada materia |
| Materias | Admin crea la materia; el director de programa gestiona su contenido -- metodologías docentes, resultados de aprendizaje y competencias asociadas, y las horas y la presencialidad de sus actividades formativas. Sus ECTS y su código RUCT los carga la importación |
| Sistemas de evaluación | Admin y el director de programa, en cada materia: código y denominación de la memoria, tipo y horquilla |
| Cursos académicos | Admin: crear, editar (solo mientras no tenga guías), activar el curso -- nace entonces una guía por asignatura de programa, clonada de la del curso anterior -- y activar el semestre. Cada guía docente pertenece a un curso académico |
| Profesorado | Admin: dar de alta, editar y dar de baja profesores de su universidad, asignarlos a asignaturas de programa y nombrar o quitar al director de un programa; cada profesor edita su propio perfil |
| Asignaturas de programa | Admin crea, da de baja, asigna el profesorado y edita todos sus campos igual que el director de programa; el director de programa edita el contenido académico -- curso, carácter, idioma, temario, requisitos previos, semestre -- y sus asociaciones de metodologías docentes, resultados de aprendizaje y actividades formativas. Admin tiene la misma paridad de edición y de asociaciones |
| Guías docentes | El profesorado redacta (temario, evaluación, bibliografía, planificación docente); el director de programa decide (aprobar, rechazar, escalar a aprobada, revocar una aprobación) y, como corrección excepcional, puede editar su temario, evaluación, bibliografía y planificación docente; Admin supervisa (consulta el estado, previsualiza y descarga el PDF) |
| Catálogo de asignaturas | Admin |
| Catálogo de metodologías docentes | El director de programa y Admin, como las competencias: cada programa tiene el suyo, con el código y la descripción de su memoria; se reparten en materias y, de las de cada materia, en sus asignaturas de programa |
| Catálogo de resultados de aprendizaje | El director de programa -- creación y reparto en materias y asignaturas de programa; Admin también puede crearlos, editarlos y eliminarlos por programa y asociarlos a asignaturas de programa |
| Catálogo de competencias | El director de programa y Admin, igual que los resultados de aprendizaje: crear, editar y eliminar por programa, y repartirlas en materias y, de las de cada materia, en sus asignaturas de programa. Los programas de memoria de formato nuevo no tienen competencias |
| Catálogo de actividades formativas | El director de programa y Admin: cada programa tiene el suyo, con el código y el nombre de su memoria; toda materia y asignatura del programa tiene una fila por actividad, con las horas (y, en la materia, la presencialidad) que se le repartan |
