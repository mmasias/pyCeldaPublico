<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Normal (queda otro RA)|Advertencia (se queda sin ninguno)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/wireframe-normal.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/wireframe-advertencia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Desasociar un `ResultadoAprendizaje` de una `AsignaturaGrado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin `<<choice>>` bloqueante, a diferencia de `desasociarResultadoAprendizajeAMateria()`**: en `Materia`, la desasociación se bloquea si alguna `AsignaturaGrado` ya usa ese `ResultadoAprendizaje` (nivel inferior de la cascada). Aquí `AsignaturaGrado` es el último escalón -- no hay un nivel estructural inferior que dependa de este reparto para bloquear la desasociación, y `Guia` no deriva en vivo de él (los RA se heredan al generar el PDF, fijados en fase estructural, no editables desde la propia `Guia`). Tampoco hay invariante de mínimo en el modelo de dominio.

Confirmación con advertencia condicional, no bloqueo: si el `ResultadoAprendizaje` que se desasocia es el único de esa `AsignaturaGrado`, el sistema lo advierte -- la guía docente que se genere sobre ella podría quedar incompleta -- pero permite confirmar igual, mismo criterio y misma discussion de cierre que [`desasignarProfesorAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md). RAK1/RAH1 para normal/advertencia son ilustrativos: la asignación real RA-`AsignaturaGrado` no está en el seed extraído.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasociarResultadoAprendizajeAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado o- ResultadoAprendizaje`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsociacionResultadoAprendizajeAsignaturaGrado()` del catálogo
- [`asociarResultadoAprendizajeAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asociación)
