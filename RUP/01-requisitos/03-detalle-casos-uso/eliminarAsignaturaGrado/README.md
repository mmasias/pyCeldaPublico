<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Extinguir una `AsignaturaGrado` del catálogo del grado (borrado lógico, no físico)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Mismo patrón que `eliminarAsignatura()`/`eliminarGrado()`, no el de `eliminarFacultad()`**: el modelo de dominio cierra que `AsignaturaGrado` (junto con `Grado` y `Asignatura`) **nunca se borra físicamente** -- usa `estado` (Vigente/Extinguido); Extinguido bloquea altas nuevas apoyadas en ella pero preserva lo existente para no romper Guías históricas. Por eso no hay rama roja de bloqueo por "tiene hijos": confirmar aquí siempre tiene éxito, el único fallo posible es la cancelación del propio actor.

Self-loop sobre `GRADO_ABIERTO` (no sobre un listado propio de `AsignaturaGrado`, que `Admin` no tiene -- ver [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md)): el retoque de [`abrirGrado()`](../abrirGrado/README.md) añade la tabla de `AsignaturaGrado` desde la que se dispara esta acción.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GRADO_ABIERTO : eliminarAsignaturaGrado()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- Modelo del dominio -- README, "Nada del catálogo se borra físicamente (`Grado`, `Asignatura`, `AsignaturaGrado`): usan `estado` (Vigente/Extinguido)"
