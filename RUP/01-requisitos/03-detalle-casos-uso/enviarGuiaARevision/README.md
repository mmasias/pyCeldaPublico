<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

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

|Éxito (suma 100%)|Error (suma != 100%)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-exito.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Enviar la `Guia` de una `AsignaturaGrado` a revisión del director de grado, exigiendo que la suma de `PonderacionEvaluacion` dé exactamente 100%|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : enviarGuiaARevision()` (éxito) y `GUIA_ABIERTO --> GUIA_ABIERTO : enviarGuiaARevision()` (rechazo por suma de ponderaciones)
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- Modelo del dominio -- `Guia *-d- PonderacionEvaluacion`, regla de suma 100% documentada en el README
- Diagrama de estados de Guia -- `Borrador -> EnRevision` / `Rechazada -> EnRevision`
