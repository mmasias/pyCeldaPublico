<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
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
|**Actor**|`DirectorGrado`|
|**Objetivo**|Desasociar un `ResultadoAprendizaje` de una `Materia`, siempre que ninguna `AsignaturaGrado` de esa `Materia` lo tenga asignado|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`<<choice>>` bloqueante por integridad de la cascada: los `ResultadoAprendizaje` de una `AsignaturaGrado` deben ser subconjunto de los ya asignados a su `Materia` (regla de consistencia del modelo del dominio) -- desasociar de `Materia` sin comprobarlo dejaría huérfano ese reparto en `AsignaturaGrado`. Mismo criterio de bloqueo que `eliminarResultadoAprendizaje()`, aplicado aquí a un nivel de la cascada en vez de al catálogo completo del `Grado`. RAK1/RAH1 para bloqueada/confirmación son ilustrativos: la asignación real `Materia`-`ResultadoAprendizaje` no está en el seed extraído.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarResultadoAprendizajeAMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- Modelo del dominio -- `AsignaturaGrado o- ResultadoAprendizaje`, README: "los `ResultadoAprendizaje` asignados a una `AsignaturaGrado` deben ser subconjunto de los ya asignados a su `Materia`" (origen de la regla de bloqueo)
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
