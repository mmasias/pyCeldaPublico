<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/README.md) / [Diseño](/RUP/03-diseño/casos-uso/descargarPlanificacionDocentePDF/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > descargarPlanificacionDocentePDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/README.md)|[Diseño](/RUP/03-diseño/casos-uso/descargarPlanificacionDocentePDF/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Aprobada o En revisión|Borrador o Rechazada|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/wireframe-borrador.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` (heredado por `DirectorPrograma`), `Admin`|
|**Objetivo**|Descargar en PDF la planificación docente de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

El documento oficial de la guía ([`descargarGuiaPDF()`](../descargarGuiaPDF/README.md)) sigue el formulario de Calidad, que no incluye la planificación docente: el profesor no tenía forma de sacar su cronograma de pyCelda. Este caso de uso genera un PDF propio con ella, a petición de Manuel.

**Contenido**: la cabecera institucional y los datos de la asignatura (asignatura, titulación, curso, semestre y docentes) del curso académico de la `Guia`; las `Sesion` **vinculadas** (las guardadas), numeradas por orden, con su descripción y el color de fila de su tipo (sin columna de tipo: el color la sustituye); y, debajo de la tabla, el total de sesiones y la leyenda de colores. Maquetación compacta para que una planificación habitual quepa en una página (hasta unas 35 sesiones; el corpus ronda las 30). `Sesion` no tiene fecha: la planificación es por número de sesión, no un calendario.

**Estado de la `Guia`**: el `<<choice>>` no bloquea; decide la marca de agua. Con la guía `EnRevision` o `Aprobada`, el PDF sale limpio: la planificación es la que el profesor envió y su uso es responsabilidad suya. En `Borrador` o `Rechazada` lleva la marca de agua diagonal "BORRADOR - NO OFICIAL", con el mismo criterio que [`previsualizarGuia()`](../previsualizarGuia/README.md). Las sesiones creadas o editadas sin guardar el borrador no entran.

**Dónde**: botón **⬇️ Descargar planificación** junto al número de sesiones, en la sección de planificación docente de [`abrirGuia()`](../abrirGuia/README.md) y en [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) (`Profesor` y `DirectorPrograma`: self-loop de `GUIA_ABIERTO` y de `PLANIFICACION_DOCENTE_ABIERTO`); para `Admin`, botón de fila en la lista de guías del programa (`GUIAS_DEL_PROGRAMA_ABIERTO`, como [`previsualizarGuia()`](../previsualizarGuia/README.md) y `descargarGuiaPDF()`, porque `Admin` no abre la guía). Mismo acceso que `descargarGuiaPDF()`: el `Profesor` que imparte la asignatura, el `DirectorPrograma` que dirige el programa y `Admin`; `404` uniforme para cualquier otro.

**Retoque del indicador de sesiones** en esas dos pantallas (mismo cambio): dentro de la sección ya no repite "Planificación docente"; dice "29 sesiones". El mínimo solo aparece con la guía en `Borrador` o `Rechazada` y sin alcanzarlo: "12 sesiones (mínimo 25)", porque es lo que impide enviar a revisión. La leyenda de colores, un punto más pequeña. El resumen de completitud del `DirectorPrograma` en revisión no cambia.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml), [de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) y [de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- mismo acceso y mismo motor de PDF
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- la tabla de sesiones y su leyenda de colores
