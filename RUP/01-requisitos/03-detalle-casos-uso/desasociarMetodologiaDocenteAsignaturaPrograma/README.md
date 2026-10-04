<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Normal (queda otra MD)|Advertencia (se queda sin ninguna)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/wireframe-normal.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/wireframe-advertencia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))|
|**Objetivo**|Desasociar una `MetodologiaDocente` de una `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

No es un borrado de entidad (la `MetodologiaDocente` sigue en el catálogo institucional, y sigue asociada a la `Materia` si lo estaba) -- es romper el vínculo a este nivel de la cascada. **Sin `<<choice>>` bloqueante, a diferencia de `desasociarMetodologiaDocenteMateria()`**: en `Materia`, la desasociación se bloquea si alguna `AsignaturaPrograma` ya usa esa `MetodologiaDocente` (nivel inferior de la cascada). Aquí `AsignaturaPrograma` es el último escalón -- no hay un nivel estructural inferior que dependa de este reparto, y `Guia` no deriva en vivo de él. Tampoco hay invariante de mínimo en el modelo de dominio.

Confirmación con advertencia condicional, no bloqueo: mismo criterio y misma discussion de cierre que [`desasignarProfesorAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md)/[`desasociarResultadoAprendizajeAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- si la `MetodologiaDocente` que se desasocia es la única de esa `AsignaturaPrograma`, el sistema lo advierte pero permite confirmar igual. MD3/MD5 son ilustrativos: la asignación real MD-`AsignaturaPrograma` no está en el seed extraído.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarMetodologiaDocenteAsignaturaPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-r- MetodologiaDocente`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del catálogo (completa el trío pendiente desde L4, resuelto como par) y del `<<choice>>` (sin bloqueo, con advertencia condicional)
- [`asociarMetodologiaDocenteAAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- caso de uso complementario (alta de la asociación)
