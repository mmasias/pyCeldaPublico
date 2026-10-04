<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > reabrirGuiaPorIncidencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/reabrirGuiaPorIncidencia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/reabrirGuiaPorIncidencia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Reabrir una `Guia` `Aprobada` cuando el `Admin` detecta una incidencia al generar su PDF|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**No implementado en código -- caso de uso solo de la fase de Requisitos.** Mismo régimen que `Requisito`/`CursoAcademico` en el modelo del dominio: representación correcta, pendiente de construir. No existe ningún endpoint de reapertura de `Guia` en `backend/app/routers/` (sin resultados para `def reabrir` en todo el backend).

Cuarta de las cuatro transiciones de reapertura desde `Aprobada` (ver [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md)), única a cargo de `Admin`. Destino `EnRevision`, nunca `Borrador`: `Admin` no tiene autoridad para asignar trabajo al `Profesor` directamente -- eso es privilegio exclusivo de `DirectorPrograma` (ver [`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md)). `Admin` solo puede escalar, no asignar: la guía aterriza en la bandeja de decisión del director, que es quien decide si hace falta corrección -- si la hace falta, el director rechaza (`EnRevision -> Rechazada`, [`rechazarGuia()`](../rechazarGuia/README.md)) y desde ahí el `Profesor` reenvía.

Reutiliza el mismo hilo `GUIAS_DEL_PROGRAMA_ABIERTO`/`GUIA_ABIERTO` que usa `DirectorPrograma` para revisión (`consultarEstadoGuias()`/`abrirGuia()`), no el de edición propia del profesor -- `Admin` no gestiona ni revisa contenido, solo necesita localizar la guía con incidencia (issue [#6](https://github.com/mmasias/pyCelda/issues/6)).

**`comentario` obligatorio** -- único caso de la familia donde no es opcional (`rechazarGuia()`/`revocarAprobacionGuia()` sí lo dejan opcional, ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44), punto 1). Decisión tomada al revisar el lote (issue [#45](https://github.com/mmasias/pyCelda/issues/45)): a diferencia de `DirectorPrograma` (que ya conoce el contenido de la guía tras revisarla, el comentario es un matiz opcional sobre una decisión ya informada), `Admin` reabre desde fuera del ciclo de revisión -- no gestiona ni revisa contenido, solo detecta una incidencia al generar el PDF. Sin `comentario` obligatorio, el `Profesor` recibiría una guía reabierta sin ninguna pista de qué falló. Mismo campo `HistorialCambio.comentario`, sin cambio en el modelo de dominio -- la obligatoriedad es una regla de este formulario concreto, no un atributo distinto. **Sin pantalla de confirmación**: mismo criterio que el resto de la familia -- ver punto 4 de la discussion #44.

Wireframe con `GII__IYA003` mostrada hipotéticamente `Aprobada` -- estado real necesario como precondición, mismo criterio ilustrativo que el resto del lote.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_PROGRAMA_ABIERTO : reabrirGuiaPorIncidencia()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Guia`
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Aprobada -> EnRevision` (`Admin`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, entrada "Reapertura desde Aprobada"
- [Issue #6](https://github.com/mmasias/pyCelda/issues/6) -- cierre del hilo de navegación reutilizado (`consultarEstadoGuias()`/`abrirGuia()`)
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, puntos 1 y 4
