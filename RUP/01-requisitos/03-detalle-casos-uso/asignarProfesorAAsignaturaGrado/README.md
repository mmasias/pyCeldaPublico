<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Asignar un `Profesor` como impartidor de una `AsignaturaGrado` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`AsignaturaGrado -- Profesor` (ver modelo del dominio) es la plantilla estable de impartición: gestionada por `Admin`, no cambia cada curso académico y admite varios profesores por `AsignaturaGrado`. Asignación libre, sin `<<choice>>` -- no hay ninguna exclusión que validar, mismo patrón que `asociarMetodologiaDocenteAMateria()`/`definirDirectorGrado()`. El selector solo excluye los `Profesor` ya asignados a esta `AsignaturaGrado`, por no tener sentido repetir la asignación.

**Exclusivo de `Admin`, no de `DirectorGrado`**: este no es un sistema de gestión de personal docente, es un sistema de gestión de guías docentes -- el director ve el profesorado asignado (`abrirAsignaturasGrado()`/`abrirAsignaturaGrado()`, ambos de solo lectura para él), pero no lo gestiona. Cierre en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asignarProfesorAAsignaturaGrado()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado -- Profesor` (plantilla estable, muchos a muchos)
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del recuento de L6, confirma el par asignar/desasignar (sin `editarAsignacion`, sin atributo propio en la relación)
- [`desasignarProfesorAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asignación)
