<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|`Admin`|`DirectorGrado`|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/wireframe-porDirectorGrado.svg)|
|<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|<sup>mismo fichero, segundo bloque `@startsalt`</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar los datos de un `Grado` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado` (`DirectorGrado --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml). Los wireframes de ambos actores ya divergían de facto en el código (`GradoAdmin.tsx` / `Grado.tsx`, componentes distintos, sin acoplamiento) -- el wireframe único original quedaba más cerca del de `Admin`; se separa ahora en dos bloques del mismo fichero, mismo patrón que la divergencia de [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) en PR [#235](https://github.com/mmasias/pyCelda/pull/235).

**`Admin` -- sin cambio**: retocado al construir L5 (mismo criterio que el retoque de `abrirMateria()` en L4, sin tocar la especificación): `GRADO_ABIERTO` es el destino del atajo plano de `AsignaturaGrado` (`crearAsignaturaGrado()`/`eliminarAsignaturaGrado()` son self-loops sobre este mismo estado, `abrirAsignaturaGrado()` es la segunda entrada -- ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)), así que el detalle del Grado necesita mostrar la tabla de `AsignaturaGrado` (agrupada por `Materia`, columna propia en la tabla) para que esos botones tengan sentido.

**`DirectorGrado` -- retocado (2026-09-05, Manuel usando el producto, relay vía pySigHor)**: la sección "Asignaturas del grado" se retira de la portada y se sustituye por el listado de `Guia` del grado (tabla + botón `[Notificar guías actualizadas]`) -- mismo contenido que ya presenta [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), duplicado a propósito. Motivo: la tabla de `AsignaturaGrado` en la portada era un duplicado exacto de la propia pestaña ["Asignaturas"](../abrirAsignaturasGrado/README.md) (mismos datos, mismo fetch) heredado sin querer del wireframe de `Admin` -- útil ahí porque da contexto a `+ Crear AsignaturaGrado`/`[Eliminar]` (exclusivos de `Admin`), puro sobrante en `DirectorGrado`. Además, llegar a una `Guia` real desde la portada exigía un clic aparte (pestaña "Guías"), y la propia tabla de asignaturas no enlazaba a ninguna `Guia` -- "ver guías es ver guías" (Manuel), lo que más aporta al entrar al grado.

**Variante conservadora, elegida explícitamente por Manuel**: `abrirGrado()` y [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) siguen siendo dos casos de uso/estados formalmente distintos (`GRADO_ABIERTO` y `GUIAS_DEL_GRADO_ABIERTO` no se fusionan, ver `diagramaContextoDirectorGrado.puml`) -- se duplica la vista, no el caso de uso. Redundancia documental aceptada a cambio de no tocar la máquina de estados; no se descarta que la portada muestre algo distinto en el futuro. Consecuencia sobre el diagrama de contexto: `GRADO_ABIERTO` gana las mismas dos transiciones de salida que ya tenía `GUIAS_DEL_GRADO_ABIERTO` -- `abrirGuia()` (por fila) y el self-loop `notificarGuiasActualizadas()`.

Sin botones hacia `Materias`/`ResultadosAprendizaje`/`AsignaturasGrado` (plural): esas transiciones llevan a un estado hijo propio, mismo criterio ya documentado en [`abrirMateria()`](../abrirMateria/README.md) para `SistemasEvaluacion` -- la navegación real a esos hijos vive en `NavGrado` (menú común a toda pantalla de `DirectorGrado` sobre un `Grado`), no modelada en ningún wireframe individual, mismo criterio que [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md)/[`consultarEstadoGuias()`](../consultarEstadoGuias/README.md).

**Nota aparte, sin tocar en este retoque**: el wireframe de [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) que este bloque reproduce ya estaba desactualizado respecto al código real -- no muestra el botón `[Notificar guías actualizadas]` ni la columna "Última actualización" que `ConsultarEstadoGuias.tsx` sí tiene. El nuevo wireframe de `DirectorGrado` aquí sí los incluye (refleja el código real, que es lo que se duplica); la staleness de la ficha vecina es preexistente y no se corrige en este PR.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`, y ahora también `GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()` / `GRADO_ABIERTO --> GRADO_ABIERTO : notificarGuiasActualizadas()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Grado`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado { codigo, estado }`
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- caso de uso cuyo contenido de pantalla se duplica aquí, sin fusionarse.
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- ahora también self-loop de `GRADO_ABIERTO`, además de `GUIAS_DEL_GRADO_ABIERTO`.
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia de wireframe entre `Admin` y `DirectorGrado` aplicado aquí.
