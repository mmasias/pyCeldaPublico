<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > aprobarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Aprobar una `Guia` que está `EnRevision`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primera de las cinco decisiones de la familia `aprobarGuia()`/`rechazarGuia()`/`escalarGuiaAAprobada()`/`revocarAprobacionGuia()`/`reabrirGuiaPorIncidencia()` -- las cinco abren `GUIA_ABIERTO` antes de decidir (reutilizando `abrirGuia()`), nunca son self-loop de listado. Ver detalle completo de los cuatro huecos de diseño resueltos en la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

**Sin campo de formulario**: a diferencia de `rechazarGuia()`/`revocarAprobacionGuia()`/`reabrirGuiaPorIncidencia()` (que narran una incidencia y sí piden `comentario`), aprobar es un "sí" sin matiz que explicar por defecto -- el sistema registra directamente `"aprobada sin incidencia"` en `HistorialCambio.comentario`, sin pedir nada al `DirectorGrado`. Decisión cerrada en el punto 1 de la discussion #44.

**Sin pantalla de confirmación**: la acción se dispara en un único paso desde `GUIA_ABIERTO`, sin `<<choice>>` ni sub-estado `ConfirmandoX` -- a diferencia de `eliminarX()` (borrado físico irreversible), esta decisión tiene su propio mecanismo de corrección ya en el catálogo (`revocarAprobacionGuia()`), así que no hace falta la pausa adicional. Decisión cerrada en el punto 4 de la discussion #44.

**Sincronización de `Guia -- Profesor` (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: pasar a `Aprobada` re-deriva `Guia -- Profesor` de la plantilla `AsignaturaGrado -- Profesor` en ese instante -- misma familia que la regeneración del PDF, un efecto de la transición, no un paso que el `DirectorGrado` decida. Es el punto de sincronización de la copia: entre aprobaciones la copia puede quedar por detrás de la plantilla si el `Admin` la cambió, y una guía que volvió a `EnRevision` por ese cambio (efecto colateral de `asignar`/`desasignarProfesorAAsignaturaGrado()`) recupera aquí la lista al día. Si `Guia.asignaturaGrado` es nula (columna nullable), no se toca `Guia -- Profesor` y la aprobación sigue su curso. Ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) y [`asignarProfesorAAsignaturaGrado()`](../asignarProfesorAAsignaturaGrado/README.md).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : aprobarGuia()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `EnRevision -> Aprobada`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, sin relación directa `DirectorGrado`-`Guia`; nota de `Guia -- Profesor` (re-derivada al aprobar, issue #254)
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- la aprobación es el punto de sincronización de `Guia -- Profesor`
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- listado del que se parte, con la misma `Guia` mostrada hipotéticamente `EnRevision`
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, puntos 1 y 4
