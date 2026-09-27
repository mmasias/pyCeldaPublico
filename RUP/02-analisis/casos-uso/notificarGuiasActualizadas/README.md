<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > notificarGuiasActualizadas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/notificarGuiasActualizadas/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/notificarGuiasActualizadas/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`notificarGuiasActualizadas()`](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/README.md): un solo paso, sin `<<choice>>`, self-loop sobre el listado completo del `Grado` -- el `DirectorGrado` solicita notificar y el sistema avisa al `Admin` de que las `Guia` de su `Grado` están listas. Sin ninguna clase de Modelo: el envío de la notificación es un mecanismo de infraestructura fuera del dominio (correo, mensajería interna...), su forma concreta pertenece a Diseño -- mismo criterio que [`eliminarReferenciaBibliografica()`](../eliminarReferenciaBibliografica/README.md), solo Vista y Controlador.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/notificarGuiasActualizadas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `NotificarGuiasActualizadasView`

**Responsabilidades:**
- recoge la solicitud de notificación sobre el `Grado` abierto.
- presenta la confirmación "Notificación enviada al Admin".

**Colaboraciones:**
- **Entrada:** `:GUIAS_DEL_GRADO_ABIERTO` -- el `DirectorGrado` solicita notificar guías actualizadas.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_GRADO_ABIERTO` -- self-loop.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- dispara el aviso al `Admin` de que las `Guia` del `Grado` están listas (`notificarGuiasActualizadas(gradoId)`) -- no lee ni muta ninguna `Guia`, ni consulta repositorio alguno: el mecanismo de envío queda fuera del alcance de Análisis.

**Colaboraciones:**
- **Entrada:** `NotificarGuiasActualizadasView`.
- **Salida:** ninguna.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/notificarGuiasActualizadas/wireframes.puml) -- fuente de verdad del paso único.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIAS_DEL_GRADO_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : notificarGuiasActualizadas()`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- quien presenta el mismo `:GUIAS_DEL_GRADO_ABIERTO` sobre el que este caso hace self-loop.
- [`eliminarReferenciaBibliografica()`](../eliminarReferenciaBibliografica/README.md) -- mismo criterio: sin ninguna clase de Modelo en su diagrama de colaboración.
