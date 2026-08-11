<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta una `AsignaturaGrado`, vinculando una `Asignatura` del catálogo a un `Grado` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Ni C→U puro (como `crearAsignatura()`) ni "pedir todo sin distinción" (como `crearResultadoAprendizaje()`): un tercer patrón, propio de `AsignaturaGrado` por ser el primer `crearX()` del catálogo con campos de dos naturalezas distintas a la vez.** De los 7 atributos propios (aparte de `estado`, que nace `Vigente`):

- **Identidad, sin valor de catálogo que heredar** (`curso`, `carácter`, `idioma`, `semestre por defecto`) -- exclusivos de `AsignaturaGrado`, no existen en `Asignatura`. Obligatorios en la creación.
- **Override sobre `Asignatura`** (`nombre`, `ects`, `contenido`) -- el modelo del dominio documenta que se heredan del catálogo si no se fijan aquí. Se muestran ya rellenos con el valor heredado y editables in situ, no diferidos a un caso de uso posterior: a diferencia de `ects`/`contenido`/`estado` en `crearAsignatura()` (que sí se difieren a `editarAsignatura()`, mismo actor en ambos casos), aquí el editor de estos overrides es un actor distinto (`DirectorGrado`, no `Admin` -- ver abajo), así que diferirlos obligaría a un segundo actor a completar de inmediato lo que el primero acaba de crear. Mostrar el valor heredado ya resuelve el caso común (sin override) sin ese salto de actor.

**Sin nota `editarAsignaturaGrado()` en la transición de salida**, excepción deliberada a la regla general de `crearX()`: la salida no aterriza en `ASIGNATURA_GRADO_ABIERTO` sino de vuelta en `GRADO_ABIERTO` (self-loop, ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `GRADO_ABIERTO --> GRADO_ABIERTO : crearAsignaturaGrado()`) -- la nueva fila aparece en la tabla de `AsignaturaGrado` añadida al retoque de [`abrirGrado()`](../abrirGrado/README.md), con su propio botón `[Abrir]`. Y aunque aterrizara en `ASIGNATURA_GRADO_ABIERTO`, `editarAsignaturaGrado()` no es acción de `Admin` (que crea) sino de `DirectorGrado` (ver [`editarAsignaturaGrado()`](../editarAsignaturaGrado/README.md)) -- la nota asume que quien crea es quien edita a continuación, aquí no se cumple.

Datos del wireframe: `Programación I` (Materia `Programación`, `GII`, curso 1) -- único ejemplo real de `AsignaturaGrado` confirmado hasta la fecha.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GRADO_ABIERTO : crearAsignaturaGrado()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, estado}`, `(Grado, Asignatura) .. AsignaturaGrado`; README, herencia de `nombre`/`ects`/`contenido` sobre `Asignatura`
