<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`|
|**Objetivo**|Desasociar un `ResultadoAprendizaje` de una `Materia`, siempre que ninguna `AsignaturaPrograma` de esa `Materia` lo tenga asignado|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`<<choice>>` bloqueante por integridad de la cascada: los `ResultadoAprendizaje` de una `AsignaturaPrograma` deben ser subconjunto de los ya asignados a su `Materia` (regla de consistencia del [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)) -- desasociar de `Materia` sin comprobarlo dejaría huérfano ese reparto en `AsignaturaPrograma`. Mismo criterio de bloqueo que `eliminarResultadoAprendizaje()`, aplicado aquí a un nivel de la cascada en vez de al catálogo completo del `Programa`. RAK1/RAH1 para bloqueada/confirmación son ilustrativos: la asignación real `Materia`-`ResultadoAprendizaje` no está en el seed extraído.

**Retocado (issue #179, 2026-09-05)**: el mensaje de bloqueo nombra las `AsignaturaPrograma` concretas en uso, en vez de un genérico "está en uso en asignaturas-en-programa de esta materia" -- mismo patrón ya construido para [`eliminarResultadoAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md) (PR #178), auditado y replicado aquí.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarResultadoAprendizajeAMateria()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje`, README: "los `ResultadoAprendizaje` asignados a una `AsignaturaPrograma` deben ser subconjunto de los ya asignados a su `Materia`" (origen de la regla de bloqueo)
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
