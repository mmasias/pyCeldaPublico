# Estructura del sistema

pyCelda organiza sus datos en dos tipos de relación distintos: una jerarquía donde cada nivel pertenece al anterior (universidad, facultad, grado, materia y lo que cuelga de ella), y catálogos que existen de forma independiente y se asignan donde haga falta (asignaturas, metodologías docentes, resultados de aprendizaje, actividades formativas). Este mapa muestra el conjunto completo y quién gestiona cada bloque, antes de entrar en el detalle de cada tarea en los tres manuales.

## El mapa

![](/images/MANUAL_USUARIO/estructuraDelSistema.svg)

- Flecha continua: el bloque de destino nace y muere con el de origen.
- Flecha discontinua: el bloque de origen es un catálogo independiente, asignado al de destino -- la misma entrada del catálogo puede usarse en varios sitios a la vez.
- Borde discontinuo: previsto en el diseño de la institución, todavía sin construir en esta versión.
- Color de cada bloque: quién lo gestiona -- leyenda completa en el propio diagrama.

## Responsables

| Bloque | Quién lo gestiona |
|---|---|
| Universidades y facultades | Admin -- previsto, todavía sin construir en esta versión |
| Grados | Admin: crear, editar el nombre, dar de baja, y nombrar o quitar director de grado |
| Materias | Admin crea la materia; el director de grado gestiona su contenido -- metodologías docentes, resultados de aprendizaje y actividades formativas asociadas |
| Sistemas de evaluación | Admin |
| Asignaturas de grado | Admin crea, da de baja, asigna el profesorado y edita los datos administrativos (materia, sesiones mínimas); el director de grado edita el contenido académico -- curso, carácter, idioma, temario, requisitos previos, semestre -- y sus asociaciones de metodologías docentes, resultados de aprendizaje y actividades formativas |
| Guías docentes | El profesorado redacta (temario, evaluación, bibliografía, planificación docente); el director de grado decide (aprobar, rechazar, revocar una aprobación, ajustar el semestre); Admin supervisa (consulta el estado, previsualiza y descarga el PDF) |
| Catálogo de asignaturas | Admin |
| Catálogo de metodologías docentes | Admin gestiona el catálogo institucional; el director de grado elige cuáles se asocian a cada materia y, dentro de ella, a cada asignatura de grado |
| Catálogo de resultados de aprendizaje | Íntegramente el director de grado -- creación y reparto en materias y asignaturas de grado |
| Catálogo de actividades formativas | Fijo, sin gestión -- el director de grado solo reparte las horas por materia y por asignatura de grado |
