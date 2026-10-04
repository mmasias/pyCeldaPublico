<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Extinguir una `AsignaturaPrograma` del catálogo del programa (borrado lógico, no físico)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Mismo patrón que `eliminarAsignatura()`/`eliminarPrograma()`, no el de `eliminarFacultad()`**: el modelo de dominio cierra que `AsignaturaPrograma` (junto con `Programa` y `Asignatura`) **nunca se borra físicamente** -- usa `estado` (Vigente/Extinguido); Extinguido bloquea altas nuevas apoyadas en ella pero preserva lo existente para no romper Guías históricas. Por eso no hay rama roja de bloqueo por "tiene hijos": confirmar aquí siempre tiene éxito, el único fallo posible es la cancelación del propio actor.

Self-loop sobre `PROGRAMA_ABIERTO` (no sobre un listado propio de `AsignaturaPrograma`, que `Admin` no tiene -- ver [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md)): el retoque de [`abrirPrograma()`](../abrirPrograma/README.md) añade la tabla de `AsignaturaPrograma` desde la que se dispara esta acción.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : eliminarAsignaturaPrograma()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Programa`, `Asignatura`, `AsignaturaPrograma`): usan `estado` (Vigente/Extinguido)"
