<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Eliminar un `ResultadoAprendizaje` del catálogo del `Grado`, siempre que no esté asignado a ninguna `Materia` ni `AsignaturaGrado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que `eliminarFacultad()`/`eliminarMetodologiaDocente()`/`eliminarMateria()`: `ResultadoAprendizaje` no tiene `estado` propio, igual que `Materia` -- vive y muere con el `Grado` que lo contiene. El bloqueo cubre los dos niveles de la cascada de asignación (`Materia o-- ResultadoAprendizaje`, `AsignaturaGrado o-- ResultadoAprendizaje`): basta con una asignación en cualquiera de los dos para bloquear, ningún RA llega a una `AsignaturaGrado` sin pasar antes por su `Materia`. RAC2/RAH2 son datos reales del plan de estudios de GII, aportados por el usuario en la [issue #23](https://github.com/mmasias/pyCelda/issues/23); elección de cuál está bloqueado/libre es ilustrativa, no una afirmación sobre asignaciones reales (esa asignación concreta es L4, sin empezar).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : eliminarResultadoAprendizaje()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `ResultadoAprendizaje`
- Modelo del dominio -- `Materia o-- ResultadoAprendizaje`, `AsignaturaGrado o-- ResultadoAprendizaje` (origen de la regla de bloqueo, cascada en dos pasos)
