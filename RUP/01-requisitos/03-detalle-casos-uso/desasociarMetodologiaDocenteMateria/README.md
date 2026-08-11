<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Desasociar una `MetodologiaDocente` de una `Materia`, siempre que ninguna `AsignaturaGrado` de esa `Materia` la tenga asignada|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

No es un borrado de entidad (la `MetodologiaDocente` sigue en el catálogo institucional) -- es romper el vínculo `MetodologiaMateria`, con `<<choice>>` bloqueante mismo patrón que `eliminarMetodologiaDocente()`/`eliminarMateria()`. El bloqueo aquí es distinto: no es "la Materia tiene hijos" sino un hallazgo de esta misma sesión -- `MetodologiaDocente` sigue la misma cascada en dos pasos que `ResultadoAprendizaje` (`AsignaturaGrado o-- MetodologiaDocente`, ver modelo del dominio), así que desasociar de `Materia` sin comprobar su uso en `AsignaturaGrado` dejaría el reparto de esa `AsignaturaGrado` sin base. MD1/MD5 para bloqueada/confirmación son ilustrativos: `MetodologiaMateria` no está en el seed extraído.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarMetodologiaDocenteMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- Modelo del dominio -- `AsignaturaGrado o-- MetodologiaDocente` (origen de la regla de bloqueo, hallazgo de esta sesión de L4)
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
