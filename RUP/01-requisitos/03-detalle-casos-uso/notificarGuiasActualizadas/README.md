<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > notificarGuiasActualizadas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Avisar al `Admin` de que todas las `Guia` del `Grado` están `Aprobada` y listas para generar el PDF|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Self-loop de `GUIAS_DEL_GRADO_ABIERTO`, no de una `Guia` concreta -- actúa sobre el conjunto completo del listado, por eso no reutiliza `abrirGuia()` como las otras cuatro decisiones (ver [`aprobarGuia()`](../aprobarGuia/README.md)). Formaliza el paso intermedio del [guión de eventos](/RUP/00-modelo-del-dominio/README.md): "cuando todas las guías del grado están `Aprobada`, el director notifica al admin, que genera las guías en PDF" -- el disparador real de [`generarGuiasPDF()`](../generarGuiasPDF/README.md).

Sin `<<choice>>` que valide "todas Aprobada" antes de notificar: esa validación real vive en `generarGuiasPDF()` (el `Admin` es quien la necesita para decidir si genera o no), no aquí -- `notificarGuiasActualizadas()` es un aviso, no una puerta de paso. El `DirectorGrado` puede notificar en cualquier momento; si notifica antes de tiempo, el `Admin` simplemente encontrará guías pendientes al intentar generar.

Wireframe con la misma `Guia` (`GII__IYA003`) mostrada hipotéticamente `Aprobada` -- estado necesario para que el escenario tenga sentido (notificar con guías aún no aprobadas sería un aviso vacío), documentado como ilustrativo igual que el resto del lote, ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

**También self-loop de `GRADO_ABIERTO`** (retoque de [`abrirGrado()`](../abrirGrado/README.md), 2026-09-05): la portada del grado duplica el listado de `Guia` de `consultarEstadoGuias()`, con el mismo botón -- mismo caso de uso, sin comportamiento nuevo, solo una segunda pantalla desde la que se dispara.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIAS_DEL_GRADO_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : notificarGuiasActualizadas()`, y ahora también `GRADO_ABIERTO --> GRADO_ABIERTO : notificarGuiasActualizadas()`
- [`abrirGrado()`](../abrirGrado/README.md) -- segunda pantalla desde la que se alcanza este mismo self-loop.
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- guión de eventos, paso "el director notifica al admin"
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- listado del que parte este self-loop
- [`generarGuiasPDF()`](../generarGuiasPDF/README.md) -- acción que este aviso dispara en el `Admin`
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, criterio de datos hipotéticos
