<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/README.md) / [Diseño](/RUP/03-diseño/casos-uso/notificarGuiasActualizadas/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > notificarGuiasActualizadas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/README.md)|[Diseño](/RUP/03-diseño/casos-uso/notificarGuiasActualizadas/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`DirectorPrograma`|
|**Objetivo**|Avisar al `Admin` de que todas las `Guia` del `Programa` están `Aprobada` y listas para generar el PDF|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Self-loop de `GUIAS_DEL_PROGRAMA_ABIERTO`, no de una `Guia` concreta -- actúa sobre el conjunto completo del listado, por eso no reutiliza `abrirGuia()` como las otras cuatro decisiones (ver [`aprobarGuia()`](../aprobarGuia/README.md)). Formaliza el paso intermedio del [guión de eventos](/RUP/00-modelo-del-dominio/README.md): "cuando todas las guías del programa están `Aprobada`, el director notifica al admin, que genera las guías en PDF" -- el disparador real de [`generarGuiasPDF()`](../generarGuiasPDF/README.md).

Sin `<<choice>>` que valide "todas Aprobada" antes de notificar: esa validación real vive en `generarGuiasPDF()` (el `Admin` es quien la necesita para decidir si genera o no), no aquí -- `notificarGuiasActualizadas()` es un aviso, no una puerta de paso. El `DirectorPrograma` puede notificar en cualquier momento; si notifica antes de tiempo, el `Admin` simplemente encontrará guías pendientes al intentar generar.

Wireframe con la misma `Guia` (`GII__IYA003`) mostrada hipotéticamente `Aprobada` -- estado necesario para que el escenario tenga sentido (notificar con guías aún no aprobadas sería un aviso vacío), documentado como ilustrativo igual que el resto del lote, ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

**También self-loop de `PROGRAMA_ABIERTO`** (retoque de [`abrirPrograma()`](../abrirPrograma/README.md), 2026-09-05): la portada del programa duplica el listado de `Guia` de `consultarEstadoGuias()`, con el mismo botón -- mismo caso de uso, sin comportamiento nuevo, solo una segunda pantalla desde la que se dispara.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `GUIAS_DEL_PROGRAMA_ABIERTO --> GUIAS_DEL_PROGRAMA_ABIERTO : notificarGuiasActualizadas()`, y ahora también `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : notificarGuiasActualizadas()`
- [`abrirPrograma()`](../abrirPrograma/README.md) -- segunda pantalla desde la que se alcanza este mismo self-loop.
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- guión de eventos, paso "el director notifica al admin"
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- listado del que parte este self-loop
- [`generarGuiasPDF()`](../generarGuiasPDF/README.md) -- acción que este aviso dispara en el `Admin`
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, criterio de datos hipotéticos
