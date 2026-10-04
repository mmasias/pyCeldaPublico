<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|`Admin`|`DirectorPrograma`|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/wireframe-porDirectorPrograma.svg)|
|<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|<sup>mismo fichero, segundo bloque `@startsalt`</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar los datos de un `Programa` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorPrograma` (`DirectorPrograma --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml). Los wireframes de ambos actores ya divergían de facto en el código (`ProgramaAdmin.tsx` / `Programa.tsx`, componentes distintos, sin acoplamiento) -- el wireframe único original quedaba más cerca del de `Admin`; se separa ahora en dos bloques del mismo fichero, mismo patrón que la divergencia de [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md) en PR [#235](https://github.com/mmasias/pyCelda/pull/235).

**`Admin` -- sin cambio**: retocado al construir L5 (mismo criterio que el retoque de `abrirMateria()` en L4, sin tocar la especificación): `PROGRAMA_ABIERTO` es el destino del atajo plano de `AsignaturaPrograma` (`crearAsignaturaPrograma()`/`eliminarAsignaturaPrograma()` son self-loops sobre este mismo estado, `abrirAsignaturaPrograma()` es la segunda entrada -- ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)), así que el detalle del Programa necesita mostrar la tabla de `AsignaturaPrograma` (agrupada por `Materia`, columna propia en la tabla) para que esos botones tengan sentido.

**`DirectorPrograma` -- retocado (2026-09-05, Manuel usando el producto, relay vía pySigHor)**: la sección "Asignaturas del programa" se retira de la portada y se sustituye por el listado de `Guia` del programa (tabla + botón `[Notificar guías actualizadas]`) -- mismo contenido que ya presenta [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), duplicado a propósito. Motivo: la tabla de `AsignaturaPrograma` en la portada era un duplicado exacto de la propia pestaña ["Asignaturas"](../abrirAsignaturasPrograma/README.md) (mismos datos, mismo fetch) heredado sin querer del wireframe de `Admin` -- útil ahí porque da contexto a `+ Crear AsignaturaPrograma`/`[Eliminar]` (exclusivos de `Admin`), puro sobrante en `DirectorPrograma`. Además, llegar a una `Guia` real desde la portada exigía un clic aparte (pestaña "Guías"), y la propia tabla de asignaturas no enlazaba a ninguna `Guia` -- "ver guías es ver guías" (Manuel), lo que más aporta al entrar al programa.

**Variante conservadora, elegida explícitamente por Manuel**: `abrirPrograma()` y [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) siguen siendo dos casos de uso/estados formalmente distintos (`PROGRAMA_ABIERTO` y `GUIAS_DEL_PROGRAMA_ABIERTO` no se fusionan, ver `diagramaContextoDirectorPrograma.puml`) -- se duplica la vista, no el caso de uso. Redundancia documental aceptada a cambio de no tocar la máquina de estados; no se descarta que la portada muestre algo distinto en el futuro. Consecuencia sobre el diagrama de contexto: `PROGRAMA_ABIERTO` gana las mismas dos transiciones de salida que ya tenía `GUIAS_DEL_PROGRAMA_ABIERTO` -- `abrirGuia()` (por fila) y el self-loop `notificarGuiasActualizadas()`.

Sin botones hacia `Materias`/`ResultadosAprendizaje`/`AsignaturasPrograma` (plural): esas transiciones llevan a un estado hijo propio, mismo criterio ya documentado en [`abrirMateria()`](../abrirMateria/README.md) para `SistemasEvaluacion` -- la navegación real a esos hijos vive en `NavPrograma` (menú común a toda pantalla de `DirectorPrograma` sobre un `Programa`), no modelada en ningún wireframe individual, mismo criterio que [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md)/[`consultarEstadoGuias()`](../consultarEstadoGuias/README.md).

**Nota aparte, sin tocar en este retoque**: el wireframe de [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) que este bloque reproduce ya estaba desactualizado respecto al código real -- no muestra el botón `[Notificar guías actualizadas]` ni la columna "Última actualización" que `ConsultarEstadoGuias.tsx` sí tiene. El nuevo wireframe de `DirectorPrograma` aquí sí los incluye (refleja el código real, que es lo que se duplica); la staleness de la ficha vecina es preexistente y no se corrige en este PR.

**Retocado el wireframe de `Admin` al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**:
- **Columna "Curso" (issue [#486](https://github.com/mmasias/pyCelda/issues/486))**: la tabla de `AsignaturaPrograma` combina ahora `curso` + `semestre_default` en un único valor (`I-s1` en vez de `1`), con el curso en números romanos (`formatearCursoSemestre()`, frontend). Mismo cambio aplicado a la tabla equivalente de [`abrirMateria()`](../abrirMateria/README.md); sin cambio de dato ni de endpoint, puro formato de presentación.
- **Sección "Directores" (issue [#492](https://github.com/mmasias/pyCelda/issues/492))**: el detalle del Programa gana una lista de los `DirectorPrograma` actuales (nombre + email, botón `[Quitar]` por fila) y un selector + botón `[Nombrar]` para darlo de alta -- **flujo alternativo** de los casos de uso ya catalogados [`definirDirectorPrograma()`](../definirDirectorPrograma/README.md)/[`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md) (hasta ahora solo invocables desde `PROFESOR_ABIERTO`), no un caso de uso nuevo: mismo objetivo de actor, misma postcondición, mismo POST/DELETE de backend, segunda vía de entrada. `PROGRAMA_ABIERTO` gana por tanto dos self-loops nuevos en el diagrama de contexto (ver Referencias).

## Notas de diseño y trazabilidad

- La sección "Directores" permite nombrar y quitar director de Programa desde aquí (issue [#492](https://github.com/mmasias/pyCelda/issues/492)), con los mismos POST/DELETE que [`definirDirectorPrograma()`](../definirDirectorPrograma/README.md) y [`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : abrirPrograma()`, y ahora también `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : definirDirectorPrograma()` / `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : quitarDirectorPrograma()` (issue #492)
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : abrirPrograma()`, y ahora también `PROGRAMA_ABIERTO --> GUIA_ABIERTO : abrirGuia()` / `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : notificarGuiasActualizadas()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Programa`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- reutilización del caso de uso por `DirectorPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa { codigo, estado }`
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- caso de uso cuyo contenido de pantalla se duplica aquí, sin fusionarse.
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- ahora también self-loop de `PROGRAMA_ABIERTO`, además de `GUIAS_DEL_PROGRAMA_ABIERTO`.
- [`definirDirectorPrograma()`](../definirDirectorPrograma/README.md) / [`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md) -- casos de uso reutilizados aquí como flujo alternativo, issue #492
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia de wireframe entre `Admin` y `DirectorPrograma` aplicado aquí.
- [Issue #486](https://github.com/mmasias/pyCelda/issues/486) / [Issue #492](https://github.com/mmasias/pyCelda/issues/492) -- origen de este retoque
