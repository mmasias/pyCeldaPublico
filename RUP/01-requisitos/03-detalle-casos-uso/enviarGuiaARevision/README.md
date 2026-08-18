<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > enviarGuiaARevision()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Éxito (suma 100%)|Error (rango o suma incorrectos)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-exito.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Enviar la `Guia` de una `AsignaturaGrado` a revisión del director de grado, exigiendo primero que no queden ítems sin guardar y, si no los hay, que las `PonderacionEvaluacion` cumplan el rango por `SistemaEvaluacion` y sumen exactamente 100%|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : enviarGuiaARevision()` (éxito) y `GUIA_ABIERTO --> GUIA_ABIERTO : enviarGuiaARevision()` (rechazo, por ítems sin guardar o por validación de ponderaciones -- ambas razones convergen al mismo estado de salida).
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- Modelo del dominio -- `Guia *-d- PonderacionEvaluacion`, regla de suma 100% documentada en el README
- Diagrama de estados de Guia -- `Borrador -> EnRevision` / `Rechazada -> EnRevision`
- **Corregido posteriormente**: la especificación pasa de un `<<choice>>` a dos encadenados -- primero comprueba que no queden ítems pendientes-sin-vincular (creados o editados en las sub-vistas de `PonderacionEvaluacion`/`ReferenciaBibliografica` sin haber pasado por `guardarBorradorGuia()`), y solo entonces valida rango por `SistemaEvaluacion` y suma total = 100%.
