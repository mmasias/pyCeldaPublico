<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > descargarPlanificacionDocentePDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/descargarPlanificacionDocentePDF/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`descargarPlanificacionDocentePDF()`](/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/README.md): el PDF de la planificación docente de una `Guia`. Sin rama de bloqueo: el estado de la `Guia` solo decide la marca de agua.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/descargarPlanificacionDocentePDF/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de análisis

### DescargarPlanificacionDocenteView (Vista)

- presenta el botón "Descargar planificación" junto al número de sesiones (guía y planificación docente) y, a `Admin`, en cada fila de la lista de guías del programa.
- entrega el documento al navegador como descarga, sin cambiar de pantalla.

### GuiaController (Control)

- obtiene la `Guia` y comprueba el acceso: `Profesor` que imparte la asignatura, `DirectorPrograma` que dirige el programa o `Admin`; si no, "no encontrada".
- pide el documento al renderizador.

### RenderizadorPlanificacionDocente (Entidad de servicio)

- compone el documento con los datos de la asignatura, la leyenda de colores y las `Sesion` vinculadas de la `Guia`, ordenadas por número, con el color de su tipo.
- pone la marca de agua "BORRADOR - NO OFICIAL" si la `Guia` está en `Borrador` o `Rechazada`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/descargarPlanificacionDocentePDF/README.md)
- [`descargarGuiaPDF()` en Análisis](../descargarGuiaPDF/README.md) -- mismo patrón, con rama de bloqueo
