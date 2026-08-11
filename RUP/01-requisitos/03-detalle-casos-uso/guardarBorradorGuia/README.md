<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > guardarBorradorGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Persistir como `Borrador` los cambios en memoria de la `Guia` abierta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso heredado por `DirectorGrado` sin cambios (`DirectorGrado --|> Profesor`) -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml), no redeclarado.

**Self-loop sobre `GUIA_ABIERTO`, no un `<<choice>>`**: a diferencia de `enviarGuiaARevision()` (que sí valida la suma de `PonderacionEvaluacion` antes de aceptar), guardar como borrador no tiene ninguna precondición que pueda rechazarlo -- siempre tiene éxito, de ahí que la especificación no necesite rama roja.

**No es un self-loop trivial**: sobre una `Guia` ya en `Borrador` o `Rechazada`, guarda sin cambiar de estado; pero si la `Guia` estaba `Aprobada`, este mismo caso de uso es el disparador real de la transición `Aprobada -> Borrador` del diagrama de estados de `Guia` -- el `Profesor` detecta un error y empieza a corregirlo sin terminar en el momento (a diferencia de `enviarGuiaARevision()`, que cubre el caso en que la corrección ya queda resuelta). El matiz se narra en prosa en la nota de la transición de salida (`estado pasa a Extinguido`-style, mismo mecanismo que usa [`eliminarAsignatura()`](../eliminarAsignatura/README.md) para narrar un cambio de estado sin abrir una rama nueva del statechart) y en la nota del wireframe -- no hace falta un `<<choice>>` ni una segunda especificación: sigue siendo una única transición.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : guardarBorradorGuia()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- misma transición heredada
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- Diagrama de estados de Guia -- `Borrador -> EnRevision`/`Rechazada -> EnRevision` no afectan a este caso; `Aprobada -> Borrador` sí, cuando el disparador es este caso de uso
- Modelo del dominio -- entrada "Reapertura desde `Aprobada`", origen del matiz `Aprobada -> Borrador`
- [`abrirGuia()`](../abrirGuia/README.md) -- pantalla compartida donde vive el botón que dispara este caso de uso
