<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/consultarHistorialCambios/README.md) / [Diseño](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarHistorialCambios()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/consultarHistorialCambios/README.md)|[Diseño](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Feed + índice de autores|Detalle de un autor|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/wireframe-autor.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Auditar los cambios registrados en `HistorialCambio` -- feed global de las últimas 50 acciones más navegación al historial completo de un autor concreto, con su rol distinguible por fila|
|**Tipo**|Primario, de apoyo (soporte a la operación, no a la enseñanza)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#392](https://github.com/mmasias/pyCelda/issues/392), origen: `HistorialCambio` existe y se escribe activamente desde 7 puntos del código -- aprobar/rechazar/escalar/revocar guía, edición de contenido, generar planificación docente, cambio de plantilla -- pero nunca se había expuesto). Manuel: "una pantalla de bitácoras con dos columnas: la primera muestra las últimas 50 acciones en crudo, la segunda una lista de autores distintos, de modo que al abrir uno se vea toda su actividad".

**Verbo `consultar`, no `abrirX()`**: mismo criterio que [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md)/[`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- lectura/monitoreo sin alta-edición-baja. A diferencia de `consultarCopiasSeguridad()`, sí depende del modelo de dominio: `HistorialCambio` (`Guia *- HistorialCambio`) es la misma capa **L8** que `PonderacionEvaluacion`/`ReferenciaBibliografica` -- existía desde el cierre original de esa capa, referenciada en reglas de negocio reales (`activarCursoAcademico()`, `cambiarMateriaAsignaturaPrograma()`, `Guia -- Profesor` re-derivado al aprobar del issue [#254](https://github.com/mmasias/pyCelda/issues/254)) sin que ningún caso de uso la expusiera hasta hoy.

**`autor_id` no es un único espacio de IDs**: se resuelve según qué campo cambió -- `campo="estado"` con el centinela `AUTOR_ADMIN_CENTINELA` (0) es `Admin`; `campo="estado"` con id real es `DirectorPrograma.id`; `campo="contenido"`/`"planificacion_docente"` es `Profesor.id`. `DirectorPrograma` no tiene `nombre` propio (tabla mínima, issue #62) -- se cruza por email contra `Profesor.nombre` cuando existe (issue [#396](https://github.com/mmasias/pyCelda/issues/396)).

**Índice de autores fusionado por email (issue [#401](https://github.com/mmasias/pyCelda/issues/401))**: `Profesor.email` y `DirectorPrograma.email` son ambos `unique` -- la misma persona con fila en las dos tablas (caso real de producción: 3 de 9 entradas eran duplicados antes del fix) fusiona en una sola entrada del índice. `Admin` queda aislado (sin email, centinela). El detalle por autor mezcla la actividad de ambas identidades cuando aplica, con una columna "Rol" que distingue bajo qué identidad actuó en cada fila -- resuelve la discriminación por rol pedida al diseñar el CU.

**Guía en formato `Asignatura@SiglaPrograma` (issue [#403](https://github.com/mmasias/pyCelda/issues/403))**: la columna Guía muestra el nombre de la `AsignaturaPrograma` más el código del `Programa` (`Programa.codigo`, ej. "GII") -- una `Guia` existe hoy en el contexto de una `AsignaturaPrograma`@`Programa`; cuando exista `CursoAcademico` (#222) escalará a un tercer nivel.

**Sin navegación desde la tabla (issue [#398](https://github.com/mmasias/pyCelda/issues/398))**: la columna Guía es texto plano, sin enlace a [`abrirGuia()`](../abrirGuia/README.md) -- "este listado tiene como propósito solo mostrar, no lo compliquemos" (Manuel). Único punto de navegación real: seleccionar un autor del índice.

**Sin `<<choice>>`, self-loop de `SISTEMA_DISPONIBLE`**: igual que `consultarCopiasSeguridad()`, ninguna precondición puede rechazar esta lectura -- un historial vacío es un estado válido (listas vacías), no un error.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> HISTORIAL_CAMBIOS_ABIERTO : consultarHistorialCambios()`, vuelta con `abrirPanelAdministracion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- package "Auditoría", `Admin -- consultarHistorialCambios`
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- precedente del verbo `consultar` para lectura/monitoreo sin CRUD
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- origen y destino de la navegación
- Issue [#392](https://github.com/mmasias/pyCelda/issues/392) -- diseño original del CU
- Issue [#396](https://github.com/mmasias/pyCelda/issues/396) -- resolución de nombre de `DirectorPrograma` cruzando por email
- Issue [#398](https://github.com/mmasias/pyCelda/issues/398) -- retiro del enlace de navegación en la columna Guía
- Issue [#401](https://github.com/mmasias/pyCelda/issues/401) -- fusión del índice de autores por email
- Issue [#403](https://github.com/mmasias/pyCelda/issues/403) -- formato `Asignatura@SiglaPrograma` de la columna Guía
