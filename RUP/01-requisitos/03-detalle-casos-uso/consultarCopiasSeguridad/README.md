<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarCopiasSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Con datos|Vacío|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/wireframe-vacia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar qué copias de seguridad de la BD existen, con su familia, fecha, tamaño y motivo -- diagnóstico de solo lectura, sin descarga|
|**Tipo**|Primario, de apoyo (soporte a la operación, no a la enseñanza)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#308](https://github.com/mmasias/pyCelda/issues/308), origen: el `Admin` no tenía forma de ver qué copias de seguridad de la BD existen). Nace del manifiesto `backups_manifest.jsonl` que `Claude-pyCelda-Prometeus` escribe en la raíz del mismo volumen donde vive `pycelda.db` -- JSON Lines, solo-append, una línea por backup (`timestamp`, `familia` `diario`/`puntual`, `archivo` informativo, `tamano_bytes`, `motivo`), unificando dos familias reales de backup (puntuales pre-deploy/pre-migración, diarios automatizados) que hasta ahora el `Admin` no podía ver desde ningún sitio.

**Verbo `consultar`, no `abrirX()`**: `CopiaSeguridad` no es una entidad de [`modeloDominio.puml`](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- es un fichero plano fuera de la BD, sin alta/edición/baja, sin `<<choice>>` de validación posible. `abrirX()`/`abrirXs()` está reservado a catálogos reales del dominio con CRUD gestionado por `Admin` (`Universidad`, `Profesor`, `SistemaEvaluacion`...). El precedente correcto es [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md): lectura de solo-monitoreo sobre un estado que el `Admin` no gestiona, solo observa.

**Alcance: listar, no descargar.** Sin endpoint de descarga de ficheros, sin exponer rutas de filesystem al cliente más allá del `archivo` informativo del manifiesto -- ese nombre no implica que se pueda abrir o descargar, es solo el dato que Prometeus registró.

**Sin `<<choice>>`, self-loop conceptual de `SISTEMA_DISPONIBLE`**: a diferencia de `enviarGuiaARevision()` o incluso de `crearPonderacionEvaluacion()`, no hay ninguna precondición que pueda rechazar esta lectura. El manifiesto ausente (instalación nueva, o backfill de Prometeus todavía no desplegado) o vacío es un **estado válido del listado** -- lista vacía, `200`, con su propio wireframe de estado vacío -- no un error. Una línea del manifiesto mal formada (JSON inválido, campo faltante -- lo escribe un script bash sin validación) se salta a nivel de backend, invisible para este caso de uso: el `Admin` nunca ve "N líneas corruptas", ve el listado de lo que sí se pudo leer.

**Fecha exacta, no `fechaImprecisa()`** (issue [#306](https://github.com/mmasias/pyCelda/issues/306)): un `Admin` diagnosticando un incidente necesita saber exactamente cuándo se hizo un backup, no "hace mucho tiempo" -- criterio opuesto al de la columna "Última actualización" de [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), donde la imprecisión es la elección correcta para la planificación del profesor. Mismo dato (`timestamp`), formato distinto a propósito según para qué se usa.

Alcanzable desde [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) (el panel de `Admin`), como el resto de áreas de catálogo -- pero sin gemelo de listado en el sentido `abrirXs()`/`abrirX()`: no hay detalle al que navegar desde una fila, es un listado plano de un solo nivel.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> COPIAS_SEGURIDAD_ABIERTO : consultarCopiasSeguridad()`, vuelta con `abrirPanelAdministracion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- package "Copias de seguridad", `Admin -- consultarCopiasSeguridad`
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo `consultar` para lectura/monitoreo sin CRUD
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- origen y destino de la navegación
- Issue [#308](https://github.com/mmasias/pyCelda/issues/308) -- origen del caso de uso, esquema del manifiesto
- Issue [#306](https://github.com/mmasias/pyCelda/issues/306) -- por qué esta pantalla no reutiliza `fechaImprecisa()`
