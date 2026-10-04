<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta una `AsignaturaPrograma`, vinculando una `Asignatura` del catálogo a un `Programa` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Corregido tras verificación cruzada con `Claude-pySigHor-SDF1` -- el wireframe original no tenía selector de `Materia`, pese a que el modelo del dominio fija `Materia *-- AsignaturaPrograma` (composición) y el esquema real exige `materia_id` no nulo. `Asignatura` (catálogo) no tiene relación con `Materia`, así que no hay forma de derivarla: se añadió el campo `Materia (*)` al wireframe, como desplegable de las Materias ya creadas para el Programa (vía `crearMateria()`, en este mismo lote), delante de `Asignatura` en el orden -- primero se elige el grupo, luego la Asignatura del catálogo dentro de ese grupo.**

**Ni C→U puro (como `crearAsignatura()`) ni "pedir todo sin distinción" (como `crearResultadoAprendizaje()`): un tercer patrón, propio de `AsignaturaPrograma` por ser el primer `crearX()` del catálogo con campos de dos naturalezas distintas a la vez.** De los 8 atributos propios (aparte de `estado`, que nace `Vigente`), **7 se capturan en el alta** -- `requisitosPrevios` (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) nace `NULL` y lo puebla el importador del seed o [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md), no este formulario (igual que el `contenido` no se rellena de verdad hasta más tarde):

- **Vínculo con `Materia`** (`materia_id`) -- no es uno de los 7 atributos propios (es relación, no atributo), pero es obligatorio: `Materia *-- AsignaturaPrograma` en el modelo del dominio. Se elige primero, antes que la Asignatura.

- **Identidad, sin valor de catálogo que heredar** (`curso`, `carácter`, `idioma`, `semestre por defecto`) -- exclusivos de `AsignaturaPrograma`, no existen en `Asignatura`. Obligatorios en la creación.
- **Override sobre `Asignatura`** (`nombre`, `ects`, `contenido`) -- el [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) documenta que se heredan del catálogo si no se fijan aquí. Se muestran ya rellenos con el valor heredado y editables in situ, no diferidos a un caso de uso posterior: a diferencia de `ects`/`contenido`/`estado` en `crearAsignatura()` (que sí se difieren a `editarAsignatura()`, mismo actor en ambos casos), aquí el editor de estos overrides es un actor distinto (`DirectorPrograma`, no `Admin` -- ver abajo), así que diferirlos obligaría a un segundo actor a completar de inmediato lo que el primero acaba de crear. Mostrar el valor heredado ya resuelve el caso común (sin override) sin ese salto de actor.

**Sin nota `editarAsignaturaPrograma()` en la transición de salida**, excepción deliberada a la regla general de `crearX()`: la salida no aterriza en `ASIGNATURA_PROGRAMA_ABIERTO` sino de vuelta en `PROGRAMA_ABIERTO` (self-loop, ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : crearAsignaturaPrograma()`) -- la nueva fila aparece en la tabla de `AsignaturaPrograma` añadida al retoque de [`abrirPrograma()`](../abrirPrograma/README.md), con su propio botón `[Abrir]`. Y aunque aterrizara en `ASIGNATURA_PROGRAMA_ABIERTO`, `editarAsignaturaPrograma()` no es acción de `Admin` (que crea) sino de `DirectorPrograma` (ver [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md)) -- la nota asume que quien crea es quien edita a continuación, aquí no se cumple.

**Efecto colateral sobre `Guia` -- `crearAsignaturaPrograma()` crea también su `Guia` vacía**: al dar de alta la `AsignaturaPrograma` nace su `Guia` en `Borrador`, con `semestre = AsignaturaPrograma.semestreDefault`, sin `PonderacionEvaluacion` ni `ReferenciaBibliografica` y con `Guia -- Profesor` vacío -- es la primera `Guia` de esa `AsignaturaPrograma`, no hay nada que clonar. Mismo criterio que [`activarCursoAcademico()`](../activarCursoAcademico/README.md) documenta para el caso "sin `Guia` del curso anterior" (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md), "Qué se clona exactamente al nacer una `Guia`..."), que aquí es el único caso posible: `crearAsignaturaPrograma()` es por definición el nacimiento de la `AsignaturaPrograma`. Simplificación actual: `CursoAcademico` no existe todavía como entidad, así que hoy la `Guia` se crea siempre, sin condición -- cuando `CursoAcademico` se construya de verdad, esta creación adquirirá la misma condición de curso activo sin rediseñar nada. Sin este efecto colateral, el `Profesor` asignado vía `asignarProfesorAAsignaturaPrograma()` no ve el botón "Abrir guía" en `/mis-asignaturas-programa` (`guia_id` llega a `None`) -- inconsistencia detectada en producción y motivo de esta documentación.

Datos del wireframe: `Programación I` (Materia `Programación`, `GII`, curso 1) -- único ejemplo real de `AsignaturaPrograma` confirmado hasta la fecha.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : crearAsignaturaPrograma()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`, `(Programa, Asignatura) .. AsignaturaPrograma`; README, herencia de `nombre`/`ects`/`contenido` sobre `Asignatura` y sección "Qué se clona exactamente al nacer una `Guia`..." (contrato que esta creación aplica al caso sin `Guia` anterior). `requisitosPrevios` (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) **no se captura en el alta**: nace `NULL` y lo puebla el importador del seed o [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md), igual que el campo `contenido` no se rellena de verdad hasta más tarde.
- [`activarCursoAcademico()`](../activarCursoAcademico/README.md) -- el otro disparador de creación de `Guia`; origen del criterio "sin `Guia` anterior que clonar -> nace vacía" que aquí se reutiliza
- [`asignarProfesorAAsignaturaPrograma()`](../asignarProfesorAAsignaturaPrograma/README.md) -- documenta el efecto colateral simétrico sobre `Guia -- Profesor` al rellenar una `Guia` nacida vacía
