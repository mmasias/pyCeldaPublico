<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Normal (queda otro RA)|Advertencia (se queda sin ninguno)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/wireframe-normal.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/wireframe-advertencia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))|
|**Objetivo**|Desasociar un `ResultadoAprendizaje` de una `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin `<<choice>>` bloqueante, a diferencia de `desasociarResultadoAprendizajeAMateria()`**: en `Materia`, la desasociación se bloquea si alguna `AsignaturaPrograma` ya usa ese `ResultadoAprendizaje` (nivel inferior de la cascada). Aquí `AsignaturaPrograma` es el último escalón -- no hay un nivel estructural inferior que dependa de este reparto para bloquear la desasociación, y `Guia` no deriva en vivo de él (los RA se heredan al generar el PDF, fijados en fase estructural, no editables desde la propia `Guia`). Tampoco hay invariante de mínimo en el modelo de dominio.

Confirmación con advertencia condicional, no bloqueo: si el `ResultadoAprendizaje` que se desasocia es el único de esa `AsignaturaPrograma`, el sistema lo advierte -- la guía docente que se genere sobre ella podría quedar incompleta -- pero permite confirmar igual, mismo criterio y misma discussion de cierre que [`desasignarProfesorAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md). RAK1/RAH1 para normal/advertencia son ilustrativos: la asignación real RA-`AsignaturaPrograma` no está en el seed extraído.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarResultadoAprendizajeAsignaturaPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsociacionResultadoAprendizajeAsignaturaPrograma()` del catálogo
- [`asociarResultadoAprendizajeAAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) -- caso de uso complementario (alta de la asociación)
