<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Normal (queda otra MD)|Advertencia (se queda sin ninguna)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/wireframe-normal.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/wireframe-advertencia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Desasociar una `MetodologiaDocente` de una `AsignaturaGrado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

No es un borrado de entidad (la `MetodologiaDocente` sigue en el catálogo institucional, y sigue asociada a la `Materia` si lo estaba) -- es romper el vínculo a este nivel de la cascada. **Sin `<<choice>>` bloqueante, a diferencia de `desasociarMetodologiaDocenteMateria()`**: en `Materia`, la desasociación se bloquea si alguna `AsignaturaGrado` ya usa esa `MetodologiaDocente` (nivel inferior de la cascada). Aquí `AsignaturaGrado` es el último escalón -- no hay un nivel estructural inferior que dependa de este reparto, y `Guia` no deriva en vivo de él. Tampoco hay invariante de mínimo en el modelo de dominio.

Confirmación con advertencia condicional, no bloqueo: mismo criterio y misma discussion de cierre que [`desasignarProfesorAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md)/[`desasociarResultadoAprendizajeAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- si la `MetodologiaDocente` que se desasocia es la única de esa `AsignaturaGrado`, el sistema lo advierte pero permite confirmar igual. MD3/MD5 son ilustrativos: la asignación real MD-`AsignaturaGrado` no está en el seed extraído.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasociarMetodologiaDocenteAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado o-r- MetodologiaDocente`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del catálogo (completa el trío pendiente desde L4, resuelto como par) y del `<<choice>>` (sin bloqueo, con advertencia condicional)
- [`asociarMetodologiaDocenteAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asociación)
